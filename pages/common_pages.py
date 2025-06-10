from selenium.webdriver.common.by import By
from utils.webevents import WebEvents, Validators

class LoginPage:
    _USERNAME_INPUT = (By.NAME, "username")
    _PASSWORD_INPUT = (By.NAME, "password")
    _LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")
    _ERROR_MESSAGE = (By.XPATH, "//p[contains(@class, 'oxd-alert-content-text')]")
    _DASHBOARD_HEADER = (By.XPATH, "//h6[text()='Dashboard']")

    def __init__(self, driver):
        self.driver = driver
        self.events = WebEvents(driver)
        self._validators = Validators(driver)

    def login_valid(self, username, password):
        self.events.enter_text(self._USERNAME_INPUT, username)
        self.events.enter_text(self._PASSWORD_INPUT, password)
        self.events.click_element(self._LOGIN_BUTTON)
        is_dashboard = self._validators.is_element_visible(self._DASHBOARD_HEADER)
        assert is_dashboard, "Dashboard not visible after login"
        return is_dashboard

    def login_invalid(self, username, password, expected_error):
        self.events.enter_text(self._USERNAME_INPUT, username)
        self.events.enter_text(self._PASSWORD_INPUT, password)
        self.events.click_element(self._LOGIN_BUTTON)
        actual_error = self.events.get_text(self._ERROR_MESSAGE)
        assert self._validators.validate_element_text(self._ERROR_MESSAGE, expected_error)
        return actual_error


class HomePage:
    _ADMIN_MENU = (By.XPATH, "//span[text()='Admin']")
    _PIM_MENU = (By.XPATH, "//span[text()='PIM']")
    _LEAVE_MENU = (By.XPATH, "//span[text()='Leave']")
    _TIME_MENU = (By.XPATH, "//span[text()='Time']")
    _RECRUITMENT_MENU = (By.XPATH, "//span[text()='Recruitment']")
    _MY_INFO_MENU = (By.XPATH, "//span[text()='My Info']")
    _PERFORMANCE_MENU = (By.XPATH, "//span[text()='Performance']")
    _DASHBOARD_MENU = (By.XPATH, "//span[text()='Dashboard']")
    _DIRECTORY_MENU = (By.XPATH, "//span[text()='Directory']")
    _MAINTENANCE_MENU = (By.XPATH, "//span[text()='Maintenance']")
    _BUZZ_MENU = (By.XPATH, "//span[text()='Buzz']")
    _USER_DROPDOWN = (By.XPATH, "//span[@class='oxd-userdropdown-tab']")
    _LOGOUT_BUTTON = (By.XPATH, "//a[text()='Logout']")

    def __init__(self, driver):
        self.driver = driver
        self.events = WebEvents(driver)
        self._validators = Validators(driver)

    def navigate_to_admin(self):
        self.events.click_element(self._ADMIN_MENU)

    def navigate_to_pim(self):
        self.events.click_element(self._PIM_MENU)

    def navigate_to_leave(self):
        self.events.click_element(self._LEAVE_MENU)

    def navigate_to_time(self):
        self.events.click_element(self._TIME_MENU)

    def navigate_to_recruitment(self):
        self.events.click_element(self._RECRUITMENT_MENU)

    def navigate_to_my_info(self):
        self.events.click_element(self._MY_INFO_MENU)

    def navigate_to_performance(self):
        self.events.click_element(self._PERFORMANCE_MENU)

    def navigate_to_dashboard(self):
        self.events.click_element(self._DASHBOARD_MENU)

    def navigate_to_directory(self):
        self.events.click_element(self._DIRECTORY_MENU)

    def navigate_to_maintenance(self):
        self.events.click_element(self._MAINTENANCE_MENU)

    def navigate_to_buzz(self):
        self.events.click_element(self._BUZZ_MENU)

    def logout(self):
        self.events.click_element(self._USER_DROPDOWN)
        self.events.click_element(self._LOGOUT_BUTTON)