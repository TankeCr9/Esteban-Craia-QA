"""
================================================================================
  QA AUTOMATION PORTFOLIO – Selenium + Python
  Author  : Esteban Gabriel Craia
  Target  : https://the-internet.herokuapp.com  (public Selenium sandbox)
  Runner  : pytest
  Install : pip install selenium pytest pytest-html webdriver-manager
================================================================================

Test Coverage:
  TC-SE-001  Login – Valid Credentials
  TC-SE-002  Login – Invalid Credentials (Negative)
  TC-SE-003  Form Authentication – Session Persistence
  TC-SE-004  Checkboxes – Toggle & Assert State
  TC-SE-005  Dropdown – Option Selection Validation
  TC-SE-006  Dynamic Loading – Wait Strategy (Explicit Wait)
  TC-SE-007  File Upload – Input Simulation
  TC-SE-008  Alerts – Accept / Dismiss / Prompt
  TC-SE-009  Hover Actions – Visibility of Hidden Elements
  TC-SE-010  Multiple Windows – Context Switching
"""

import time
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


# ─── Constants ────────────────────────────────────────────────────────────────

BASE_URL = "https://the-internet.herokuapp.com"
VALID_USER = "tomsmith"
VALID_PASS = "SuperSecretPassword!"
IMPLICIT_WAIT = 10
EXPLICIT_WAIT = 15


# ─── Fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture(scope="function")
def driver():
    """
    Provides a configured ChromeDriver instance per test.
    Headless mode enabled for CI/CD compatibility.
    """
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--log-level=3")  # Suppress browser noise

    service = Service(ChromeDriverManager().install())
    drv = webdriver.Chrome(service=service, options=options)
    drv.implicitly_wait(IMPLICIT_WAIT)
    drv.maximize_window()

    yield drv

    drv.quit()


def wait(driver, timeout=EXPLICIT_WAIT):
    """Helper – returns a configured WebDriverWait instance."""
    return WebDriverWait(driver, timeout)


# ─── TC-SE-001 ─────────────────────────────────────────────────────────────────

class TestLogin:
    """Functional tests for the Form Authentication page."""

    def test_TC_SE_001_login_valid_credentials(self, driver):
        """
        TC-SE-001
        Scenario : User logs in with valid credentials.
        Expected : Redirected to /secure, success flash message displayed.
        """
        driver.get(f"{BASE_URL}/login")

        wait(driver).until(EC.visibility_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        wait(driver).until(EC.url_contains("/secure"))
        flash = wait(driver).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )

        assert "/secure" in driver.current_url, "TC-SE-001 FAIL: Not redirected to /secure"
        assert "You logged into a secure area!" in flash.text, \
            f"TC-SE-001 FAIL: Unexpected flash message: {flash.text}"
        print("✅ TC-SE-001 PASS: Valid login successful")

    def test_TC_SE_002_login_invalid_credentials(self, driver):
        """
        TC-SE-002
        Scenario : User logs in with wrong password.
        Expected : Stays on /login, error flash message displayed.
        """
        driver.get(f"{BASE_URL}/login")

        wait(driver).until(EC.visibility_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys("wrong_user")
        driver.find_element(By.ID, "password").send_keys("wrong_pass")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        flash = wait(driver).until(
            EC.visibility_of_element_located((By.ID, "flash"))
        )

        assert "Your username is invalid!" in flash.text, \
            f"TC-SE-002 FAIL: Expected error message, got: {flash.text}"
        assert "/secure" not in driver.current_url, \
            "TC-SE-002 FAIL: Should not navigate to /secure on invalid credentials"
        print("✅ TC-SE-002 PASS: Invalid login blocked correctly")

    def test_TC_SE_003_session_persistence_after_login(self, driver):
        """
        TC-SE-003
        Scenario : After login, user navigates away and back – session should persist.
        Expected : /secure page still accessible without re-login.
        """
        # Login
        driver.get(f"{BASE_URL}/login")
        wait(driver).until(EC.visibility_of_element_located((By.ID, "username")))
        driver.find_element(By.ID, "username").send_keys(VALID_USER)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        wait(driver).until(EC.url_contains("/secure"))

        # Navigate away
        driver.get(BASE_URL)
        time.sleep(1)

        # Go back to secure
        driver.get(f"{BASE_URL}/secure")
        heading = wait(driver).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h2"))
        )

        assert "Secure Area" in heading.text, \
            f"TC-SE-003 FAIL: Session not persisted. Found: {heading.text}"
        print("✅ TC-SE-003 PASS: Session persisted after navigation")


# ─── TC-SE-004 ─────────────────────────────────────────────────────────────────

class TestCheckboxes:
    """Tests for checkbox interaction and state validation."""

    def test_TC_SE_004_checkbox_toggle_and_assert(self, driver):
        """
        TC-SE-004
        Scenario : Toggle both checkboxes and verify state changes.
        Expected : Each checkbox changes state correctly after click.
        """
        driver.get(f"{BASE_URL}/checkboxes")

        checkboxes = wait(driver).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='checkbox']"))
        )

        assert len(checkboxes) == 2, f"TC-SE-004 FAIL: Expected 2 checkboxes, found {len(checkboxes)}"

        initial_states = [cb.is_selected() for cb in checkboxes]

        for cb in checkboxes:
            cb.click()

        new_states = [cb.is_selected() for cb in checkboxes]

        for i, (before, after) in enumerate(zip(initial_states, new_states)):
            assert before != after, \
                f"TC-SE-004 FAIL: Checkbox {i+1} state did not toggle (was {before}, still {after})"

        print(f"✅ TC-SE-004 PASS: States before={initial_states} → after={new_states}")


# ─── TC-SE-005 ─────────────────────────────────────────────────────────────────

class TestDropdown:
    """Tests for dropdown/select element interactions."""

    def test_TC_SE_005_dropdown_select_by_visible_text(self, driver):
        """
        TC-SE-005
        Scenario : Select 'Option 2' from dropdown.
        Expected : 'Option 2' is selected and reflected in the element.
        """
        driver.get(f"{BASE_URL}/dropdown")

        dropdown_element = wait(driver).until(
            EC.presence_of_element_located((By.ID, "dropdown"))
        )
        select = Select(dropdown_element)

        # Assert initial state
        assert select.first_selected_option.text == "Please select an option", \
            "TC-SE-005 FAIL: Unexpected initial option selected"

        select.select_by_visible_text("Option 2")
        assert select.first_selected_option.text == "Option 2", \
            f"TC-SE-005 FAIL: Expected 'Option 2', got '{select.first_selected_option.text}'"

        # Also validate all options exist
        options = [o.text for o in select.options]
        assert "Option 1" in options and "Option 2" in options, \
            "TC-SE-005 FAIL: Missing expected options in dropdown"

        print("✅ TC-SE-005 PASS: Dropdown selection validated")


# ─── TC-SE-006 ─────────────────────────────────────────────────────────────────

class TestDynamicLoading:
    """Tests demonstrating Explicit Wait strategy for async content."""

    def test_TC_SE_006_wait_for_dynamic_element(self, driver):
        """
        TC-SE-006
        Scenario : Click 'Start' on Dynamic Loading Example 2.
        Expected : 'Hello World!' text appears after loading spinner disappears.
        Strategy : Explicit Wait – waits up to 15s for element visibility.
        """
        driver.get(f"{BASE_URL}/dynamic_loading/2")

        start_btn = wait(driver).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#start button"))
        )
        start_btn.click()

        # Wait for loading spinner to disappear
        wait(driver, timeout=20).until(
            EC.invisibility_of_element_located((By.ID, "loading"))
        )

        # Wait for result to appear
        result = wait(driver, timeout=20).until(
            EC.visibility_of_element_located((By.ID, "finish"))
        )

        assert "Hello World!" in result.text, \
            f"TC-SE-006 FAIL: Expected 'Hello World!', got '{result.text}'"
        print("✅ TC-SE-006 PASS: Dynamic content loaded and validated")


# ─── TC-SE-007 ─────────────────────────────────────────────────────────────────

class TestFileUpload:
    """Tests for file input element interaction."""

    def test_TC_SE_007_file_upload_success(self, driver, tmp_path):
        """
        TC-SE-007
        Scenario : Upload a test file via file input element.
        Expected : Filename appears in the upload confirmation area.
        """
        # Create temp file
        test_file = tmp_path / "qa_test_upload.txt"
        test_file.write_text("QA Test File – Esteban Craia Portfolio")

        driver.get(f"{BASE_URL}/upload")

        file_input = wait(driver).until(
            EC.presence_of_element_located((By.ID, "file-upload"))
        )
        file_input.send_keys(str(test_file))

        driver.find_element(By.ID, "file-submit").click()

        result = wait(driver).until(
            EC.visibility_of_element_located((By.ID, "uploaded-files"))
        )

        assert "qa_test_upload.txt" in result.text, \
            f"TC-SE-007 FAIL: Uploaded filename not confirmed. Got: '{result.text}'"
        print("✅ TC-SE-007 PASS: File upload confirmed")


# ─── TC-SE-008 ─────────────────────────────────────────────────────────────────

class TestAlerts:
    """Tests for browser alert, confirm, and prompt dialogs."""

    def test_TC_SE_008_alert_accept(self, driver):
        """
        TC-SE-008
        Scenario : Trigger JS alert and accept it.
        Expected : Alert text matches expected, dialog dismissed.
        """
        driver.get(f"{BASE_URL}/javascript_alerts")

        alert_btn = wait(driver).until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[text()='Click for JS Alert']")
            )
        )
        alert_btn.click()

        alert = wait(driver).until(EC.alert_is_present())
        alert_text = alert.text
        assert "I am a JS Alert" in alert_text, \
            f"TC-SE-008 FAIL: Unexpected alert text: '{alert_text}'"
        alert.accept()

        result = driver.find_element(By.ID, "result")
        assert "You successfuly clicked an alert" in result.text, \
            f"TC-SE-008 FAIL: Result text not updated: '{result.text}'"
        print("✅ TC-SE-008 PASS: Alert accepted and result validated")


# ─── TC-SE-009 ─────────────────────────────────────────────────────────────────

class TestHoverActions:
    """Tests for mouse hover interactions using ActionChains."""

    def test_TC_SE_009_hover_reveals_hidden_element(self, driver):
        """
        TC-SE-009
        Scenario : Hover over a user figure card.
        Expected : Hidden caption (name + link) becomes visible.
        """
        driver.get(f"{BASE_URL}/hovers")

        figures = wait(driver).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "figure"))
        )

        assert len(figures) >= 3, f"TC-SE-009 FAIL: Expected 3 figures, found {len(figures)}"

        actions = ActionChains(driver)
        actions.move_to_element(figures[0]).perform()
        time.sleep(0.5)

        caption = figures[0].find_element(By.CLASS_NAME, "figcaption")
        assert caption.is_displayed(), "TC-SE-009 FAIL: Caption not visible after hover"

        name = caption.find_element(By.TAG_NAME, "h5").text
        assert "user" in name.lower(), \
            f"TC-SE-009 FAIL: Expected 'user' in name, got '{name}'"
        print(f"✅ TC-SE-009 PASS: Hover revealed caption: '{name}'")


# ─── TC-SE-010 ─────────────────────────────────────────────────────────────────

class TestWindowHandling:
    """Tests for multi-window context switching."""

    def test_TC_SE_010_new_window_context_switch(self, driver):
        """
        TC-SE-010
        Scenario : Click link that opens a new browser window.
        Expected : Switch to new window, validate content, switch back.
        """
        driver.get(f"{BASE_URL}/windows")

        original_handle = driver.current_window_handle
        link = wait(driver).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Click Here"))
        )
        link.click()

        wait(driver, timeout=10).until(EC.number_of_windows_to_be(2))

        all_handles = driver.window_handles
        new_handle = [h for h in all_handles if h != original_handle][0]

        driver.switch_to.window(new_handle)
        heading = wait(driver).until(
            EC.visibility_of_element_located((By.TAG_NAME, "h3"))
        )
        assert "New Window" in heading.text, \
            f"TC-SE-010 FAIL: Expected 'New Window', got '{heading.text}'"

        driver.close()
        driver.switch_to.window(original_handle)

        assert "windows" in driver.current_url, \
            "TC-SE-010 FAIL: Did not return to original window"
        print("✅ TC-SE-010 PASS: Multi-window navigation validated")
