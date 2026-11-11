# NaukriAutoUpdater

A lightweight Python automation script that uses [Playwright](https://playwright.dev/python/) to open your Naukri profile, make a minimal change to the Resume Headline, and save it in an attempt to refresh profile activity.

The project supports a one-time manual login setup and reuses a local persistent Chromium browser profile for subsequent runs.

> **Important:** This project is independent and is not affiliated with, endorsed by, or supported by Naukri. It does not guarantee that Naukri will display an “Active Today” status. Review Naukri's current terms and policies before using browser automation.

## What it does

When run normally, the script:

1. Launches Chromium using a persistent browser profile.
2. Opens the Naukri profile edit page.
3. Checks whether the browser has been redirected to a login page.
4. Opens the Resume Headline editor.
5. Adds a trailing period to the headline, or removes the trailing period if one is already present.
6. Saves the headline.

The script prints a success message when the save button is clicked. That message confirms the automation reached the save action, not that Naukri has independently confirmed a particular activity status.

## Requirements

- Python 3.9 or later is recommended.
- pip, the Python package installer.
- Playwright for Python.
- Chromium installed through Playwright.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/iShahrukhParvez/NaukriAutoUpdater.git
cd NaukriAutoUpdater
```

### 2. Create and activate a virtual environment (recommended)

**Windows (PowerShell):**

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Python dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Install the Chromium browser

```bash
python -m playwright install chromium
```

## First-time setup

Run the script with the `setup` argument:

```bash
python update_naukri.py setup
```

A Chromium window will open on the Naukri login page.

1. Log in manually using your Naukri account.
2. Complete any OTP or verification steps shown by Naukri.
3. Wait until your profile dashboard is visible.
4. Return to the terminal and press **Enter**.
5. The script closes the browser and retains the persistent browser profile for later runs.

Do not close the browser before pressing Enter in the terminal.

## Run the updater

After completing the first-time setup, run:

```bash
python update_naukri.py
```

The script reuses the saved browser profile and attempts to update the Resume Headline.

If the session expires or the script redirects to the login page, repeat the first-time setup:

```bash
python update_naukri.py setup
```


## Schedule automatic runs on Windows

You can use **Windows Task Scheduler** to run the script automatically at a chosen time. The script itself does not contain a scheduler; Task Scheduler starts it for you.

### Before scheduling

1. Complete the first-time login setup manually:

   ```powershell
   python update_naukri.py setup
   ```

2. Confirm that a normal run works:

   ```powershell
   python update_naukri.py
   ```

3. Find the full paths to:
   - Your Python executable. If you use a virtual environment, use the executable inside `.venv\Scripts\python.exe`.
   - `update_naukri.py` in your cloned repository.

   For example:

   ```text
   Python executable (Virtual Environment):
   C:\Users\YourName\NaukriAutoUpdater\.venv\Scripts\python.exe

   Python executable (System Installation):
   C:\Users\YourName\AppData\Local\Programs\Python\Python314\python.exe

   Script: C:\Users\YourName\NaukriAutoUpdater\update_naukri.py
   ```


   Replace these example paths with the actual paths on your computer.

### Create a scheduled task

1. Open the Windows **Start** menu, search for **Task Scheduler**, and open it.
2. In the Actions pane, select **Create Basic Task**.
3. Enter a name such as `NaukriAutoUpdater`, optionally add a description, and select **Next**.
4. Choose a trigger, for example **Daily**, then select **Next**.
5. Choose the start date and time, and set the recurrence interval. Select **Next**.
6. Choose **Start a program**, then select **Next**.
7. Fill in the action fields:

   **Program/script**

   Enter the full path to your Python executable, for example:

   ```text
   C:\Users\YourName\NaukriAutoUpdater\.venv\Scripts\python.exe
   ```

   **Add arguments (optional)**

   Enter the full path to the script in quotes:

   ```text
   "C:\Users\YourName\NaukriAutoUpdater\update_naukri.py"
   ```

   **Start in (optional)**

   Enter the project folder path, without quotes:

   ```text
   C:\Users\YourName\NaukriAutoUpdater
   ```

8. Select **Next**, review the task details, and select **Finish**.

### Recommended task settings

After creating the task, find it in **Task Scheduler Library**, right-click it, and select **Properties**.

- Under **General**, select **Run only when user is logged on**. This is the recommended starting point because the script launches a visible Chromium browser and uses the signed-in Windows user's local browser profile.
- Under **Settings**, consider enabling **If the task is already running, then the following rule applies: Do not start a new instance**. This helps prevent overlapping runs.
- Keep your computer powered on and awake at the scheduled time. A task cannot run while the computer is shut down. If your power settings allow it, Task Scheduler can be configured to wake the computer, but availability depends on the device and Windows configuration.

### Test and manage the task

- In Task Scheduler Library, right-click `NaukriAutoUpdater` and select **Run** to test it.
- Check **Last Run Result** and **History** in Task Scheduler if it does not run as expected. You may need to enable task history from the Actions pane.
- To change the schedule, open the task's **Properties** and edit the **Triggers** tab.
- To stop future runs, right-click the task and select **Disable** or **Delete**.

**Important:** Complete the manual login setup before scheduling. Do not schedule the `setup` command. Schedule only the normal command shown above. Your Windows account must have access to the project folder and the saved browser profile. The computer must be available at the scheduled time, and Naukri session expiry or website changes may require manual attention. Use a schedule that respects Naukri's current terms and policies.

## Browser profile and account security

The script stores its persistent Chromium profile in your home directory:

```text
~/.naukri_browser_profile
```

This location is resolved using Python's `os.path.expanduser("~")`, so the actual path depends on your operating system and user account.

**Treat this directory as sensitive.** It may contain cookies and other browser data that allow access to your signed-in account.

- Never commit the browser profile to Git.
- Do not share or upload the profile directory.
- Do not copy it to an untrusted computer.
- Log out of the account and remove the local profile if you no longer want to retain the session.

The script does not ask you to put your Naukri password or OTP in the source code.

## Troubleshooting

### Playwright is not installed

Activate your virtual environment, then run:

```bash
python -m pip install -r requirements.txt
```

### Chromium is not installed

Run:

```bash
python -m playwright install chromium
```

### The login session has expired

Run the setup command again and complete the login manually:

```bash
python update_naukri.py setup
```

### The Resume Headline editor cannot be found

Naukri may change its page layout or element selectors. The script relies on page selectors that may need maintenance when the website changes.

### The script reports an automation error

Read the error printed in the terminal. If the page structure has changed, inspect the current Naukri page and review the relevant Playwright selectors in `update_naukri.py`.

## Current behavior and limitations

- The script uses a visible Chromium browser. During normal execution, it attempts to position the browser window off-screen. This is not headless execution.
- The script does not include a scheduler. Run it manually or use an operating-system scheduler if you understand and accept the implications of automating your account.
- The script makes a small, real change to the Resume Headline by toggling a trailing period.
- The script does not verify that Naukri has updated the displayed activity status after saving.
- Website changes, login challenges, or policy changes may prevent the script from working.

## Responsible use

Use this project only with an account you are authorized to access. Respect Naukri's terms, rate limits, and security checks. Do not use it to misrepresent your activity or bypass access controls.

## Disclaimer

This software is provided “as is”, without warranty of any kind. You are responsible for reviewing the website's rules and deciding whether to use the automation. The author is not responsible for account restrictions, unexpected profile changes, or other consequences arising from its use.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
