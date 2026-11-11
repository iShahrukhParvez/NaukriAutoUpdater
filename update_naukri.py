import os
import sys
import time
from playwright.sync_api import sync_playwright

# Folder where your login session cookies will be stored securely
PROFILE_DIR = os.path.join(os.path.expanduser("~"), ".naukri_browser_profile")

def run_bot(setup_mode=False):
    with sync_playwright() as p:
                
        print("Launching browser...")
        
        # Setup mode runs visibly so you can type; daily automation runs invisibly (headless/minimized) 
        headless_setting = False 
        
        # Determine window placement arguments based on mode
        chrome_args = ["--disable-blink-features=AutomationControlled"]
        
        # If running automated in headful mode, boot the window off-screen
        if not headless_setting and not setup_mode:
            print("💡 Running headful session in the background workspace...")
            chrome_args.extend([
                "--window-position=-2000,-2000", # Moves the physical window completely off-screen
                "--no-first-run"
            ])
            
        context = p.chromium.launch_persistent_context(
            user_data_dir=PROFILE_DIR,
            headless=headless_setting,
            args=chrome_args
        )
        
        # Use existing page or create a new one
        page = context.pages[0] if context.pages else context.new_page()
        
        # Explicitly enforce standard viewport limits so layout elements aren't altered
        page.set_viewport_size({"width": 1280, "height": 800})


        if setup_mode:
            print("\n========================================================")
            print("▶️ SETUP MODE: Opening Naukri. Please log in manually.")
            print("========================================================")
            page.goto("https://www.naukri.com/nlogin/login", wait_until="load")
            
            print("\n👉 DO NOT CLOSE THE BROWSER YET.")
            print("👉 Enter your credentials/OTP on the webpage now.")
            print("👉 Once you see your profile dashboard, come back here.")
            input("\n✅ Press [ENTER] here in the terminal ONLY AFTER you are successfully logged in... ")
            
            print("Saving session and closing...")
            context.close()
            print("🎉 Setup complete! You can now run the regular scheduler.")
            return

                # --- REGULAR AUTOMATION FLOW ---
        print("Navigating directly to your Naukri Profile Edit page...")
        # Going directly to the edit page bypasses home page popups and layout shifts
        page.goto("https://www.naukri.com/mnjuser/profile", wait_until="load")
        time.sleep(5) # Give dynamic widgets time to render
        
        if "login" in page.url:
            print("❌ Error: Session expired or not logged in. Please re-run: python update_naukri.py setup")
            context.close()
            return

        print("Refreshing profile state via resume headline...")
        try:
            # Optimized selector: Looks for the edit pencil inside the resume headline section
            # If the specific container fails, it falls back to a text-based search
            edit_button = page.locator('span:has-text("Resume headline") ~ span.edit, .resumeHeadline .edit, [target="_blank"] + .edit').first
            
            # Wait up to 5 seconds for the button to appear instead of a full 30 seconds
            edit_button.wait_for(timeout=5000)
            edit_button.click()
            time.sleep(2)
            
            # Locate input text area
            headline_input = page.locator("#resumeHeadlineTxt")
            current_text = headline_input.input_value()
            
            # Make a micro-change (toggle a trailing dot)
            new_text = current_text.rstrip(".") if current_text.endswith(".") else current_text + "."
                
            headline_input.fill(new_text)
            time.sleep(1)
            
            # Click Save button
            save_button = page.locator('button.btn-dark-ot[type="submit"]:has-text("Save")').first
            save_button.wait_for(state="visible", timeout=5000)
            save_button.click()
            print("✅ Success: Profile headline save action completed.")
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Automation Error: {e}")
            
        context.close()

if __name__ == "__main__":
    # Check if user passed "setup" argument
    if len(sys.argv) > 1 and sys.argv[1].lower() == "setup":
        run_bot(setup_mode=True)
    else:
        run_bot(setup_mode=False)
