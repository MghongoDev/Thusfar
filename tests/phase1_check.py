"""Phase 1 checks, run through the room.

1. Both agents reply in the room under their own names.
2. The scribe creates a room document.
3. After `!reset`, the builder reads that room document in a fresh turn.

Each run uses a new document name, so the scribe must create it rather than
update an old one. The scribe picks a secret word, writes it only in the
document, and keeps it out of the chat. If the builder can name the word
after `!reset`, it read the document, since the chat never held the word.

Usage: python3 tests/phase1_check.py --team p1

Issues: #7 (Phase 1 close-out, part of #2). ADR: 0001.
"""

from __future__ import annotations

import argparse
import re
import secrets
import sys
import time

from driver import Room, text_from


def check_hello(room: Room, scribe: str, builder: str) -> bool:
    since = room.post(f"@{scribe} @{builder} say hello in one line each, and name your role.")
    replies = room.wait_for(since, [scribe, builder], timeout=240)
    ok = bool(text_from(replies, scribe)) and bool(text_from(replies, builder))
    report("both agents reply", ok, replies)
    return ok


def check_document_read(room: Room, scribe: str, builder: str) -> list[bool]:
    document = f"CHECK-{secrets.token_hex(3).upper()}"
    start = room.post(
        f"@{scribe} create a new room document named {document}. Choose one secret "
        f"word yourself, a common English noun, and write only this line in it: "
        f"'Secret word: <your word>'. Do not post the word in this chat. "
        f"Reply with the document's name when it is done."
    )
    made = room.wait_for(start, [scribe], timeout=240)
    created = document in text_from(made, scribe)
    report(f"scribe creates the room document {document}", created, made)

    since = room.post(f"!reset @{builder}")
    room.wait_for(since, [], timeout=40, quiet=15)
    time.sleep(5)

    since = room.post(
        f"@{builder} what is the secret word in the room document named {document}? "
        f"Read the document and answer with the word."
    )
    answer = room.wait_for(since, [builder], timeout=240)
    builder_said = text_from(answer, builder).lower()

    since = room.post(f"@{scribe} what secret word did you write in {document}? Answer with the word only.")
    told = room.wait_for(since, [scribe], timeout=240)
    words = re.findall(r"[a-z]+", text_from(told, scribe).lower())
    word = words[-1] if words else ""

    before_builder = " ".join(r.text.lower() for r in room.replies_since(start) if r.at < answer[0].at) if answer else ""
    leaked = bool(word) and re.search(rf"\b{word}\b", before_builder) is not None
    read = bool(word) and not leaked and re.search(rf"\b{word}\b", builder_said) is not None
    report(f"builder reads the word {word!r} from {document} after !reset (leaked to chat: {leaked})", read, answer + told)
    return [created, read]


def report(name: str, ok: bool, replies) -> None:
    print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    for r in replies:
        if r.text.strip():
            print(f"    {r.author}: {r.text[:300]!r}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--team", default="thusfar")
    args = ap.parse_args()
    scribe, builder = f"{args.team}-scribe", f"{args.team}-builder"
    room = Room(f"{args.team}-decisions")
    results = [check_hello(room, scribe, builder), *check_document_read(room, scribe, builder)]
    return 0 if all(results) else 1


if __name__ == "__main__":
    sys.exit(main())
