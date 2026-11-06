# Install Switch Console on Linux

This guide installs Switch Console on Fedora, x86_64, and starts its local server. Linux builds are early access.

## Before you start

- Docker, with the Docker Compose plugin. Check with `docker compose version`.
- Your user in the `docker` group. Check with `id -nG`. If it is missing, run `sudo usermod -aG docker $USER`, then log out and back in.
- Claude Code, signed in. Check with `claude auth status`.

Podman does not work in place of Docker. Console calls the `docker` binary.

## Steps

1. Start Docker:

   ```bash
   sudo systemctl enable --now docker
   ```

2. Install the Console:

   ```bash
   sudo dnf install https://github.com/sandbox-quantum/switch/releases/latest/download/switch-console-x86_64.rpm
   ```

   On Debian or Ubuntu, use the `.deb` from the same releases page.

3. Launch it with these flags:

   ```bash
   switch-console --ozone-platform=x11 --disable-gpu --password-store=gnome-libsecret
   ```

   The first two flags stop a blank window under Wayland. The third lets Console save your sign-ins.

4. Select **Get started**, then **On this computer**, then **Start**. Wait for "Local server is running".

5. Open **Settings**, then **Agent providers**, and select **Recheck**. Claude Code should show as signed in.

## If something goes wrong

| Symptom | Cause and fix |
|---|---|
| Blank window | Wayland. Quit with `pkill -x switch-console` and relaunch with the flags in step 3. |
| Closing the window leaves Console running | Expected on Linux. Quit with `pkill -x switch-console`. |
| Sign-ins are lost on restart | No secret service. Launch with `--password-store=gnome-libsecret`. |
| Console says Docker is not installed | The Compose plugin is missing, or you are not in the `docker` group. |
| The server starts but has no Mattermost | Docker was not running when the server started. Start Docker, then restart the server. |

The flags apply to one launch only. To keep them, copy the Console's `.desktop` file to `~/.local/share/applications/` and add the flags to its `Exec` line.
