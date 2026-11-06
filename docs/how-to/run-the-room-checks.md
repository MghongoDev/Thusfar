# Run the room checks

The checks post to a Thusfar room as you would, wait for the agents, and test their replies. They need Python 3.10 or later and nothing else.

## Before you start

- A room made from the template. Note the `team` value you used.
- Your Mattermost sign-in. In Switch Console, open **Home**, find the row under **Messaging apps**, and select **Sign-in details…**.

## Steps

1. Create `.env.local` at the repo root. Git ignores it.

   ```
   MM_URL=http://localhost:42247
   MM_USER=your-mattermost-username
   MM_PASSWORD=your-mattermost-password
   ```

   Instead of `MM_USER` and `MM_PASSWORD`, you can give `MM_TOKEN`, a Mattermost personal access token.

   `MM_URL` is the address of the bundled Mattermost. The port can change when the server restarts; the Mattermost link in Console shows the current one.

2. Run the Phase 1 checks, with your `team` value:

   ```bash
   python3 tests/phase1_check.py --team thusfar
   ```

Each check prints `PASS` or `FAIL`, then every reply it saw. The script exits with 0 only when all checks pass.

## What the Phase 1 checks do

| Check | Passes when |
|---|---|
| Both agents reply | Each agent answers a hello under its own name. |
| The scribe creates the room document | The scribe names a new room document, such as `CHECK-3F9A1C`, in its reply. Each run picks a new name, so the scribe must create the document, not update one. |
| The builder reads the room document after `!reset` | With its context cleared, the builder names the secret word the scribe wrote in the document. The word never appears in the chat, so the builder can only have read it from the document. |

Each run leaves a `CHECK-...` room document and a few test messages behind. Run the checks in a room you will throw away, not in your demo room.

## If something goes wrong

| Message | Fix |
|---|---|
| `Missing MM_URL, MM_USER, MM_PASSWORD` | Create `.env.local` as in step 1. |
| `POST /users/login failed: 401` | The username or password is wrong. Copy them again from **Sign-in details…**. |
| `No channel named ...-decisions` | The room does not exist, or your user is not in it. Check the `team` value. |
| A check fails with no replies | The agents did not wake. Check that both show as online in Console. |
