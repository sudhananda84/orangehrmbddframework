from selenium.webdriver.common.by import By
from utils.webevents import WebEvents, Validators

class PIMPage:
    _PIM_HEADER = (By.XPATH, "//h6[text()='PIM']")
    _ADD_BUTTON = (By.XPATH, "//button[text()=' Add ']")
    _SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    _SEARCH_BUTTON = (By.XPATH, "//button[text()='Search']")
    _RESET_BUTTON = (By.XPATH, "//button[text()='Reset']")
    _EMPLOYEE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    _EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div/input")
    _EMPLOYEE_LIST_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div")
    _EDIT_BUTTON = (By.XPATH, ".//button[@title='Edit']")
    _DELETE_BUTTON = (By.XPATH, ".//button[@title='Delete']")
    _CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[text()='Yes, Delete']")
    _PROFILE_HEADER = (By.XPATH, "//h6[contains(text(),'Personal Details')]")
    _FIRST_NAME_INPUT = (By.NAME, "firstName")
    _LAST_NAME_INPUT = (By.NAME, "lastName")
    _EMPLOYEE_TABLE = ("id", "employee-table")
    _ERROR_MSG = (By.CSS_SELECTOR, ".oxd-alert-content-text")

    def __init__(self, driver):
        self.driver = driver
        self.events = WebEvents(driver)
        self._validators = Validators(driver)

    def is_pim_page_displayed(self):
        return self._validators.is_element_visible(self._PIM_HEADER)

    def add_employee(self, first_name, last_name, employee_id=None):
        self.events.click_element(self._ADD_BUTTON)
        self.events.enter_text(self._FIRST_NAME_INPUT, first_name)
        self.events.enter_text(self._LAST_NAME_INPUT, last_name)
        if employee_id:
            self.events.clear_field(self._EMPLOYEE_ID_INPUT)
            self.events.enter_text(self._EMPLOYEE_ID_INPUT, employee_id)
        self.events.click_element(self._SAVE_BUTTON)
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def search_employee(self, name=None, emp_id=None):
        if name:
            self.events.enter_text(self._EMPLOYEE_NAME_INPUT, name)
        if emp_id:
            self.events.enter_text(self._EMPLOYEE_ID_INPUT, emp_id)
        self.events.click_element(self._SEARCH_BUTTON)
        return self.get_employee_list()

    def reset_search_filters(self):
        self.events.click_element(self._RESET_BUTTON)

    def get_employee_list(self):
        rows = self.driver.find_elements(*self._EMPLOYEE_LIST_ROWS)
        employees = []
        for row in rows:
            columns = row.find_elements(By.XPATH, ".//div[@role='cell']")
            if columns:
                employees.append([col.text for col in columns])
        return employees

    def select_employee_by_name(self, name):
        rows = self.driver.find_elements(*self._EMPLOYEE_LIST_ROWS)
        for row in rows:
            if name in row.text:
                row.click()
                return True
        return False

    def edit_personal_details(self, name, **details):
        if not self.select_employee_by_name(name):
            return False
        if 'first_name' in details:
            self.events.enter_text((By.NAME, "firstName"), details['first_name'])
        if 'last_name' in details:
            self.events.enter_text((By.NAME, "lastName"), details['last_name'])
        if 'dob' in details:
            self.events.enter_text((By.XPATH, "//input[@placeholder='yyyy-mm-dd']"), details['dob'])
        if 'gender' in details:
            gender_xpath = f"//label[text()='{details['gender']}']/preceding-sibling::input"
            self.events.click_element((By.XPATH, gender_xpath))
        self.events.click_element(self._SAVE_BUTTON)
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def edit_contact_details(self, name, **contact_details):
        if not self.select_employee_by_name(name):
            return False
        self.events.click_element((By.XPATH, "//a[text()='Contact Details']"))
        if 'address' in contact_details:
            self.events.enter_text((By.NAME, "street1"), contact_details['address'])
        if 'city' in contact_details:
            self.events.enter_text((By.NAME, "city"), contact_details['city'])
        if 'mobile' in contact_details:
            self.events.enter_text((By.NAME, "mobile"), contact_details['mobile'])
        if 'email' in contact_details:
            self.events.enter_text((By.NAME, "email"), contact_details['email'])
        self.events.click_element(self._SAVE_BUTTON)
        return True

    def edit_experience_details(self, name, **experience_details):
        if not self.select_employee_by_name(name):
            return False
        self.events.click_element((By.XPATH, "//a[text()='Qualifications']"))
        if 'company' in experience_details:
            self.events.click_element((By.XPATH, "//button[text()='Add']"))
            self.events.enter_text((By.NAME, "employer"), experience_details['company'])
        if 'job_title' in experience_details:
            self.events.enter_text((By.NAME, "jobtitle"), experience_details['job_title'])
        if 'from_date' in experience_details:
            self.events.enter_text((By.NAME, "fromDate"), experience_details['from_date'])
        if 'to_date' in experience_details:
            self.events.enter_text((By.NAME, "toDate"), experience_details['to_date'])
        self.events.click_element(self._SAVE_BUTTON)
        return True

    def edit_employee(self, name, new_details):
        rows = self.driver.find_elements(*self._EMPLOYEE_LIST_ROWS)
        for row in rows:
            if name in row.text:
                edit_btn = row.find_element(*self._EDIT_BUTTON)
                edit_btn.click()
                if 'first_name' in new_details:
                    self.events.enter_text(self._FIRST_NAME_INPUT, new_details['first_name'])
                if 'last_name' in new_details:
                    self.events.enter_text(self._LAST_NAME_INPUT, new_details['last_name'])
                self.events.click_element(self._SAVE_BUTTON)
                return self._validators.is_element_visible(self._PROFILE_HEADER)
        return False

    def delete_employee(self, name):
        rows = self.driver.find_elements(*self._EMPLOYEE_LIST_ROWS)
        for row in rows:
            if name in row.text:
                delete_btn = row.find_element(*self._DELETE_BUTTON)
                delete_btn.click()
                self.events.click_element(self._CONFIRM_DELETE_BUTTON)
                return True
        return False

    def delete_multiple_employees(self, names):
        results = {}
        for name in names:
            result = self.delete_employee(name)
            results[name] = result
        return results

    def is_employee_profile_displayed(self):
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def is_employee_present(self, first_name, last_name, employee_id):
        # Implement logic to search employee in the table
        return self._validators.validate_employee_creation(
            [first_name, last_name, employee_id]
        )

    def is_experience_details_updated(self, name, company, job_title, from_date, to_date):
        return self._validators.validate_table_contains(
            self._EMPLOYEE_TABLE,
            [name, company, job_title, from_date, to_date]
        )

    def is_contact_details_updated(self, name, address, city, mobile, email):
        return self._validators.validate_table_contains(
            self._EMPLOYEE_TABLE,
            [name, address, city, mobile, email]
        )

    def is_personal_details_updated(self, name, dob, gender):
        # Validate updated details in the table or profile section
        return self._validators.validate_table_contains(
            self._EMPLOYEE_TABLE,
            [name, dob, gender]
        )

    def is_error_displayed(self, locator =None,  message="" ):
        if locator is None:
            locator = self._ERROR_MSG
        return self._validators.validate_text_present(locator, message)
