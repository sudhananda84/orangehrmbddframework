
import time
import random
from pyexpat.errors import messages

from selenium.webdriver.common.by import By
from utils.webevents import WebEvents, Validators

class RecruitmentPage:
    _RECRUITMENT_HEADER = (By.XPATH, "//h6[text()='Recruitment']")
    _ADD_BUTTON = (By.XPATH, "//button[text()=' Add ']")
    _SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    _SEARCH_BUTTON = (By.XPATH, "//button[text()=' Search ']")
    _RESET_BUTTON = (By.XPATH, "//button[text()='Reset']")
    _CANDIDATE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    _CANDIDATE_EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/../following-sibling::div/input")
    _CANDIDATE_LIST_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div")
    _EDIT_BUTTON = (By.XPATH, ".//button[contains(@class,'oxd-icon-button') and .//i[contains(@class,'pencil')]]")
    _DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[text()=' Yes, Delete ']")
    _PROFILE_HEADER = (By.XPATH, "//h6[contains(text(),'Candidate Details')]")
    _FIRST_NAME_INPUT = (By.NAME, "firstName")
    _LAST_NAME_INPUT = (By.NAME, "lastName")
    _EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/../following-sibling::div/input")
    _VACANCY_SELECT = (By.XPATH, "//label[text()='Vacancy']/../following-sibling::div//div[contains(@class,'oxd-select-text')]")
    _ERROR_MSG = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    def __init__(self, driver):
        self.driver = driver
        self.events = WebEvents(driver)
        self._validators = Validators(driver)

    def is_recruitment_page_displayed(self):
        return self._validators.is_element_visible(self._RECRUITMENT_HEADER)

    def add_candidate(self, first_name, last_name, email, vacancy=None):
        self.events.click_element(self._ADD_BUTTON)
        self.events.enter_text(self._FIRST_NAME_INPUT, first_name)
        self.events.enter_text(self._LAST_NAME_INPUT, last_name)
        self.events.enter_text(self._EMAIL_INPUT, email)
        if vacancy:
            self.events.click_element(self._VACANCY_SELECT)
            self.events.select_dropdown_option(self._VACANCY_SELECT, vacancy)
        self.events.click_element(self._SAVE_BUTTON)
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def search_candidate(self, name=None, email=None):
        if name:
            self.events.enter_text(self._CANDIDATE_NAME_INPUT, name)
        if email:
            self.events.enter_text(self._CANDIDATE_EMAIL_INPUT, email)
        self.events.click_element(self._SEARCH_BUTTON)
        return self.get_candidate_list()

    def reset_search_filters(self):
        self.events.click_element(self._RESET_BUTTON)

    def get_candidate_list(self):
        rows = self.driver.find_elements(*self._CANDIDATE_LIST_ROWS)
        candidates = []
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//div[@role='cell']")
            if columns:
                candidates.append([col.text for col in columns])
        print(f"Candidate list: {candidates}")
        return candidates

    def click_edit_candidate_by_name(self, name):
        self.events.click_element((By.XPATH, f"//div[text()='{name}']/../following-sibling::div//i[contains(@class,'pencil')]/parent::button"))

    def edit_candidate(self, name, new_details):
        rows = self.driver.find_elements(*self._CANDIDATE_LIST_ROWS)
        for row in rows:
            if name in row.text:
                edit_btn = row.find_element(*self._EDIT_BUTTON)
                edit_btn.click()
                if 'first_name' in new_details:
                    self.events.enter_text(self._FIRST_NAME_INPUT, new_details['first_name'])
                if 'last_name' in new_details:
                    self.events.enter_text(self._LAST_NAME_INPUT, new_details['last_name'])
                if 'email' in new_details:
                    self.events.enter_text(self._EMAIL_INPUT, new_details['email'])
                self.events.click_element(self._SAVE_BUTTON)
                return self._validators.is_element_visible(self._PROFILE_HEADER)
        return False

    def delete_multiple_candidates(self):
        self.events.is_element_displayed(self._CANDIDATE_LIST_ROWS)
        rows = self.driver.find_elements(*self._CANDIDATE_LIST_ROWS)
        selected_rows = random.sample(rows, 3)
        candidate_names = []
        for row in selected_rows:
            self.events.click_element(element=row.find_element(By.XPATH, ".//div[@role='cell'][1]//input[@type='checkbox']"))
            candidate_names.append(row.find_element(By.XPATH, ".//div[@role='cell'][2]").text)
        self.events.click_element((By.XPATH, "//button[.=' Delete Selected ']"))
        assert self.is_error_displayed(message="The selected record will be permanently deleted. Are you sure you want to continue?")
        self.events.click_element(self._DELETE_CONFIRM_BUTTON)
        self.events.is_element_displayed(self._CANDIDATE_LIST_ROWS)
        return candidate_names

    def delete_candidate(self, candidate_name):
        self.events.click_element((By.XPATH, f"//div[@class='oxd-table-cell oxd-padding-cell']/div[normalize-space(text())='{candidate_name}']/../following-sibling::div//i[contains(@class,'trash')]/parent::button"))
        time.sleep(5)
        assert self.is_error_displayed(message="The selected record will be permanently deleted. Are you sure you want to continue?")
        self.events.click_element(self._DELETE_CONFIRM_BUTTON)
        time.sleep(10)

    def check_candidate_deleted(self, candidate_name):
        self.events.enter_text(self._CANDIDATE_NAME_INPUT, candidate_name)
        self.events.click_element(self._SEARCH_BUTTON)
        time.sleep(10)
        return self.is_error_displayed(locator="//label[text()='Candidate Name']/../following-sibling::span", message="Invalid")



    def is_candidate_profile_displayed(self):
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def is_candidate_present(self, full_name):
        return self.validate_candidate_creation(full_name)

    def is_error_displayed(self, locator=None, message=""):
        if locator is None and message:
            locator = (By.XPATH, f"//*[text()='{message}']")
        elif locator is None:
            locator = self._ERROR_MSG
        print(f"Checking for error message with locator: {locator} and message: {message}")
        return self._validators.validate_text_present(locator, message)

    def validate_candidate_creation(self, full_name):
        # candidate_details: [first_name, last_name, email]
        rows = self.driver.find_elements(By.XPATH, "//div[@class='oxd-table-body']/div")
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//div[@role='cell']")
            if not columns:
                continue
            row_text = [col.text.strip() for col in columns]
            if full_name in row_text:
                return True
        return False