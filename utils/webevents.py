import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException, NoSuchElementException, ElementNotInteractableException, ElementClickInterceptedException, StaleElementReferenceException
)

class WebEvents:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def click_element(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
        except (TimeoutException, ElementClickInterceptedException, ElementNotInteractableException, StaleElementReferenceException) as e:
            print(f"Error clicking element {locator}: {e}")
            raise

    def enter_text(self, locator, text):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            element.send_keys(text)
        except (TimeoutException, ElementNotInteractableException, StaleElementReferenceException) as e:
            print(f"Error entering text in element {locator}: {e}")
            raise

    def get_text(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error getting text from element {locator}: {e}")
            raise

    def clear_field(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            element.clear()
            if element.get_attribute("value") != "":
                element.click()
                self.driver.execute_script("arguments[0].value = '';", element)
        except (TimeoutException, ElementNotInteractableException, StaleElementReferenceException) as e:
            print(f"Error clearing field {locator}: {e}")
            raise

    def is_element_displayed(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_displayed()
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error checking display status of element {locator}: {e}")
            return False

    def get_element_attribute(self, locator, attribute):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute)
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            print(f"Error getting attribute '{attribute}' from element {locator}: {e}")
            raise

class Validators:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    def is_element_displayed(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.is_displayed()
        except Exception:
            return False

    def is_element_visible(self, locator):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.is_displayed()
        except Exception:
            return False

    def validate_element_text(self, locator, expected_text):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return element.text == expected_text
        except Exception:
            return False

    def validate_element_attribute(self, locator, attribute, expected_value):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(locator)
            )
            return element.get_attribute(attribute) == expected_value
        except Exception:
            return False

    def validate_table_contains(self, table_locator, values):
        try:
            table = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located(table_locator)
            )
            rows = table.find_elements(By.TAG_NAME, "tr")
            for row in rows:
                row_text = row.text
                if all(str(val) in row_text for val in values):
                    return True
            return False
        except Exception:
            return False

    def validate_employee_creation(self, values):
        try:
            page_num = 0
            while self.is_element_displayed((By.XPATH,"//i[contains(@class,'bi-chevron-right')]/parent::button")):
                self.driver.find_elements(By.XPATH, "//button[contains(@class,'oxd-pagination-page-item--page')]")[page_num].click()
                page_num += 1
                time.sleep(10)
                rows = self.driver.find_elements(By.XPATH, "//div[@class ='oxd-table-body'] // div[@ role='row']")
                for row in rows:
                    row_text = row.text
                    if all(str(val) in row_text for val in values):
                        return True
            return False
        except Exception:
            return False


    def validate_text_present(self, locator, expected_text):
        try:
            element = WebDriverWait(self.driver, self.timeout).until(
                EC.visibility_of_element_located(locator)
            )
            return expected_text in element.text
        except Exception:
            return False

