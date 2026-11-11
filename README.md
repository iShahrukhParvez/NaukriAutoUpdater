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

## Schedule Automatic Runs on Windows

You can use **Windows Task Scheduler** to run NaukriAutoUpdater automatically at your preferred time. The script itself does not contain a scheduler. Windows Task Scheduler handles the scheduling.

### Before scheduling

1. Complete the first-time login setup manually:

   ```powershell
   python update_naukri.py setup
   ```

2. Confirm that a normal run works:

   ```powershell
   python update_naukri.py
   ```

3. Identify the full paths to your Python executable and project script.

   **If using a virtual environment:**

   Activate your environment:

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

   Then run:

   ```powershell
   python -c "import sys; print(sys.executable)"
   ```

   **If using system-installed Python:**

   Run the same command without activating a virtual environment:

   ```powershell
   python -c "import sys; print(sys.executable)"
   ```

   Copy the path displayed in the terminal.

   You also need the full path to `update_naukri.py` inside your cloned repository.

### Create a Scheduled Task

1. Open the Windows Start menu, search for **Task Scheduler**, and open it.
2. In the Actions pane, select **Create Basic Task**.
3. Enter a name such as `NaukriAutoUpdater` and select Next.
4. Choose a trigger, such as **Daily**, and select Next.
5. Configure your preferred start date, time, and recurrence interval.
6. Choose **Start a program** and select Next.
7. Configure the following fields:

   **Program/script**

   Enter the full path to your Python executable.

   Example using a virtual environment:

   ```text
   C:\Users\YourName\NaukriAutoUpdater\.venv\Scripts\python.exe
   ```

   Example using system-installed Python:

   ```text
   C:\Users\YourName\AppData\Local\Programs\Python\Python314\python.exe
   ```

   Use the path returned by the PowerShell command on your own computer.

   **Add arguments (optional)**

   Enter the full path to the Python script, enclosed in quotes:

   ```text
   "C:\Users\YourName\NaukriAutoUpdater\update_naukri.py"
   ```

   **Start in (optional)**

   Enter the project directory without quotes:

   ```text
   C:\Users\YourName\NaukriAutoUpdater
   ```

8. Select Next, review the task details, and select Finish.

### Recommended Task Settings

After creating the task:

1. Open Task Scheduler Library.
2. Right-click `NaukriAutoUpdater` and select Properties.
3. Under **General**, select **Run only when user is logged on**. This is recommended because the script launches a visible Chromium browser.
4. Under **Settings**, select **If the task is already running, then the following rule applies: Do not start a new instance**. This prevents overlapping executions.

Keep your computer powered on and available at the scheduled time. If the computer is shut down, the task cannot execute.

### Test and Manage the Scheduled Task

- Right-click the task and select **Run** to test it.
- Check the Last Run Result and Task History if the task does not run as expected.
- To change the schedule, open Properties and edit the Triggers tab.
- To stop future executions, right-click the task and select Disable or Delete.

**Important Notes:**

- Complete the manual login setup before scheduling. Do not schedule the `setup` command.
- Schedule only the normal `update_naukri.py` execution.
- Use the same Windows user account that completed the initial login setup, so the saved browser profile remains accessible.
- The computer must be awake and available at the scheduled time.
- Task Scheduler's Last Run Result does not independently confirm that Naukri updated your profile. Check the script output when testing manually.
- If your Naukri session expires or the website changes, manual attention may be required.
- Use a schedule that respects Naukri's current terms and policies.

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
