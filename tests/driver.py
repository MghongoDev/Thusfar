"""Drive a Thusfar room through Mattermost, as a human would.

Thusfar is tested only through the room itself (spec #1, Testing Decisions).
This module logs in as the human, posts to the room, and collects what the
agents reply. It uses only the Python standard library.

Settings come from `.env.local` at the repo root, which git ignores:
MM_URL, and either MM_TOKEN (a personal access token) or MM_USER and
MM_PASSWORD.

Issues: #7 (Phase 1 close-out, part of #2); #11 added attached files; #13 added saving a run; #14 added scribe_list and waits for real messages. ADRs: 0001, 0002. Reused by #5 (Phase 4).
"""

from __future__ import annotations

import json
import os
import re
import pathlib
import time
import urllib.error
import urllib.request
from dataclasses import dataclass

REPO = pathlib.Path(__file__).resolve().parent.parent



def load_settings(path: pathlib.Path = REPO / ".env.local") -> dict[str, str]:
    """Read KEY=VALUE lines. Real environment variables win."""
    settings: dict[str, str] = {}
    if path.exists():
        for line in path.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                settings[key.strip()] = value.strip().strip('"').strip("'")
    for key in ("MM_URL", "MM_TOKEN", "MM_USER", "MM_PASSWORD"):
        if os.environ.get(key):
            settings[key] = os.environ[key]
    need = ["MM_URL"] + ([] if settings.get("MM_TOKEN") else ["MM_USER", "MM_PASSWORD"])
    missing = [k for k in need if not settings.get(k)]
    if missing:
        raise SystemExit(
            f"Missing {', '.join(missing)} in {path} or the environment. "
            "Give MM_URL and either MM_TOKEN, or MM_USER and MM_PASSWORD."
        )
    return settings


@dataclass
class Reply:
    author: str
    text: str
    at: int  # Mattermost create_at, in milliseconds
    files: tuple[str, ...] = ()  # names of files attached to the post
    file_ids: tuple[str, ...] = ()


class Room:
    """One Mattermost channel that mirrors a Switch room."""

    def __init__(self, room_name: str, settings: dict[str, str] | None = None):
        self.settings = settings or load_settings()
        self.base = self.settings["MM_URL"].rstrip("/") + "/api/v4"
        self.token = self._login()
        self.me = self._get("/users/me")
        self.channel = self._find_channel(room_name)
        self._names: dict[str, str] = {}

    # HTTP ---------------------------------------------------------------

    def _request(self, method: str, path: str, body: dict | None = None, timeout: float = 30):
        data = json.dumps(body).encode() if body is not None else None
        req = urllib.request.Request(self.base + path, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if getattr(self, "token", None):
            req.add_header("Authorization", f"Bearer {self.token}")
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                payload = resp.read()
                return resp, (json.loads(payload) if payload else None)
        except urllib.error.HTTPError as err:
            raise SystemExit(f"{method} {path} failed: {err.code} {err.read()[:300]!r}")

    def download(self, file_id: str) -> bytes:
        """The bytes of a file attached to a post."""
        req = urllib.request.Request(f"{self.base}/files/{file_id}")
        req.add_header("Authorization", f"Bearer {self.token}")
        with urllib.request.urlopen(req, timeout=60) as resp:
            return resp.read()

    def save_run(self, since: int, folder: pathlib.Path) -> None:
        """Save every post after `since`, the human's included, as a transcript, with the files posted."""
        folder.mkdir(parents=True, exist_ok=True)
        data = self._get(f"/channels/{self.channel['id']}/posts?since={since}")
        posts = sorted((data["posts"][pid] for pid in data["order"]), key=lambda p: p["create_at"])
        lines = []
        for p in posts:
            if p["create_at"] <= since or p.get("type", "") != "" or not (is_message(p["message"]) or p.get("file_ids")):
                continue
            who = self.me["username"] if p["user_id"] == self.me["id"] else self._author(p)
            lines.append(f"**{who}:**\n\n{p['message'].strip()}\n")
            for fid, name in zip(p.get("file_ids") or [], _file_names(p)):
                name = pathlib.Path(name).name or "file"
                (folder / name).write_bytes(self.download(fid))
                lines.append(f"_Posted file: [{name}]({name})_\n")
        (folder / "transcript.md").write_text("\n".join(lines))

    def _get(self, path: str):
        return self._request("GET", path)[1]

    def _login(self) -> str:
        if self.settings.get("MM_TOKEN"):
            return self.settings["MM_TOKEN"]
        resp, _ = self._request(
            "POST",
            "/users/login",
            {"login_id": self.settings["MM_USER"], "password": self.settings["MM_PASSWORD"]},
        )
        token = resp.headers.get("Token")
        if not token:
            raise SystemExit("Login gave no session token.")
        return token

    def _find_channel(self, room_name: str) -> dict:
        wanted = room_name.lower()
        for team in self._get("/users/me/teams"):
            for ch in self._get(f"/users/me/teams/{team['id']}/channels"):
                if wanted in (ch["name"].lower(), ch["display_name"].lower()):
                    return ch
        raise SystemExit(f"No channel named {room_name!r} that {self.me['username']} can see.")

    def _author(self, post: dict) -> str:
        """Who wrote a post: the name it is shown under, else its Mattermost user."""
        shown_as = (post.get("props") or {}).get("override_username")
        if shown_as:
            return shown_as
        uid = post["user_id"]
        if uid not in self._names:
            self._names[uid] = self._get(f"/users/{uid}")["username"]
        return self._names[uid]

    # What a human does ----------------------------------------------------

    def post(self, text: str) -> int:
        """Post as the human. Returns the post's timestamp."""
        # Switch reads each post before Mattermost answers, which can be slow.
        body = {"channel_id": self.channel["id"], "message": text}
        _, post = self._request("POST", "/posts", body, timeout=180)
        return post["create_at"]

    def replies_since(self, since: int) -> list[Reply]:
        """Every post after `since` that the human did not write, oldest first."""
        data = self._get(f"/channels/{self.channel['id']}/posts?since={since}")
        posts = [data["posts"][pid] for pid in data["order"]]
        out = [
            Reply(self._author(p), p["message"], p["create_at"], _file_names(p), tuple(p.get("file_ids") or ()))
            for p in posts
            if p["create_at"] > since and p["user_id"] != self.me["id"] and p.get("type", "") == ""
        ]
        return sorted(out, key=lambda r: r.at)

    def wait_for(
        self,
        since: int,
        agents: list[str],
        timeout: float = 300,
        quiet: float = 25,
        poll: float = 3,
    ) -> list[Reply]:
        """Wait until every agent in `agents` has replied, then until the room goes quiet.

        Agents often post a progress line before the real answer, so we keep
        reading until no new reply has arrived for `quiet` seconds.
        """
        deadline = time.monotonic() + timeout
        replies: list[Reply] = []
        last_new = time.monotonic()
        while time.monotonic() < deadline:
            fresh = self.replies_since(since)
            if len(fresh) > len(replies):
                replies, last_new = fresh, time.monotonic()
            heard = all(any(r.author == a and (r.files or is_message(r.text)) for r in replies) for a in agents)
            if heard and time.monotonic() - last_new >= quiet:
                break
            time.sleep(poll)
        return replies


def _file_names(post: dict) -> tuple[str, ...]:
    files = (post.get("metadata") or {}).get("files") or []
    if files:
        return tuple(f.get("name", "") for f in files)
    return tuple("(unnamed file)" for _ in post.get("file_ids") or [])


def is_message(text: str) -> bool:
    """A real message, not one of Switch's progress lines."""
    t = text.strip()
    progress = ("**Worked for", "**Working", "Starting a session", "Resetting my session")
    return bool(t) and not t.startswith(progress)


def files_from(replies: list[Reply], agent: str) -> list[str]:
    """Names of every file one agent posted."""
    return [name for r in replies if r.author == agent for name in r.files]


def text_from(replies: list[Reply], agent: str) -> str:
    """Everything one agent said, joined."""
    return "\n".join(r.text for r in replies if r.author == agent)


def report(name: str, ok: bool, replies: list[Reply], width: int = 400) -> None:
    """Print one check's result, then every non-empty reply it saw."""
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    for r in replies:
        if r.text.strip():
            print(f"    {r.author}: {r.text[:width]!r}")


def scribe_list(room: Room, scribe: str) -> dict[int, str]:
    """The active decisions, from the scribe's `list` reply: decision ID number to its line.

    The spec reads the log this way. The newest decision is always active,
    so the highest ID here is the highest in the log.
    """
    since = room.post(f"@{scribe} list")
    replies = room.wait_for(since, [scribe], timeout=300)
    found: dict[int, str] = {}
    for line in text_from(replies, scribe).splitlines():
        m = re.match(r"\W*D-(\d{3})", line)  # only lines that start with an ID
        if m:
            found.setdefault(int(m.group(1)), line)
    return found


def decision_id(number: int) -> str:
    """The decision ID for a number: 5 is D-005."""
    return f"D-{number:03d}"
