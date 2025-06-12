import time
import random

from selenium.webdriver.common.by import By
from utils.webevents import WebEvents, Validators

class PIMPage:
    _PIM_HEADER = (By.XPATH, "//h6[text()='PIM']")
    _ADD_BUTTON = (By.XPATH, "//button[text()=' Add ']")
    _SAVE_BUTTON = (By.XPATH, "//button[@type='submit']")
    _SEARCH_BUTTON = (By.XPATH, "//button[text()=' Search ']")
    _RESET_BUTTON = (By.XPATH, "//button[text()='Reset']")
    _EMPLOYEE_NAME_INPUT = (By.XPATH, "//input[@placeholder='Type for hints...']")
    _EMPLOYEE_ID_INPUT = (By.XPATH, "//label[text()='Employee Id']/../following-sibling::div/input")
    _EMPLOYEE_LIST_ROWS = (By.XPATH, "//div[@class='oxd-table-body']/div")
    _EDIT_BUTTON = (By.XPATH, ".//button[@title='Edit']")
    _DELETE_CONFIRM_BUTTON = (By.XPATH, "//button[text()=' Yes, Delete ']")
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
        if employee_id is not None:
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
        print(f"Employee list: {employees}")
        return employees

    def click_edit_employee_by_name(self, name):
        self.events.click_element((By.XPATH, f"//div[text()='{name}']/../following-sibling::div//i[contains(@class,'pencil')]/parent::button"))


    def edit_personal_details(self, name, **details):
        self.click_edit_employee_by_name(name)

        if 'first_name' in details:
            self.events.enter_text((By.NAME, "firstName"), details['first_name'])
        if 'last_name' in details:
            self.events.enter_text((By.NAME, "lastName"), details['last_name'])
        if 'dob' in details:
            print("i am in dob section")
            self.events.enter_text((By.XPATH, "//label[text()='Date of Birth']/../following-sibling::div//input[@placeholder='yyyy-dd-mm']"), details['dob'])
        if 'gender' in details:
            gender_xpath = f"//label[text()='{details['gender']}']/input"
            self.events.click_element((By.XPATH, gender_xpath))
        self.events.click_element(self._SAVE_BUTTON)
        return self._validators.is_element_visible(self._PROFILE_HEADER)

    def edit_contact_details(self, name, **contact_details):
        self.click_edit_employee_by_name(name)

        self.events.click_element((By.XPATH, "//a[text()='Contact Details']"))
        time.sleep(10)
        if 'address' in contact_details:
            self.events.enter_text((By.XPATH, "//label[text()='Street 1']/../following-sibling::div/input"), contact_details['address'])
        if 'city' in contact_details:
            self.events.enter_text((By.XPATH, "//label[text()='City']/../following-sibling::div/input"), contact_details['city'])
        if 'mobile' in contact_details:
            self.events.enter_text((By.XPATH, "//label[text()='Mobile']/../following-sibling::div/input"), contact_details['mobile'])
        if 'email' in contact_details:
            self.events.enter_text((By.XPATH, "//label[text()='Work Email']/../following-sibling::div/input"), contact_details['email'])
        time.sleep(10)
        self.events.click_element(self._SAVE_BUTTON)
        return True

    def edit_experience_details(self, name, **experience_details):
        if not self.click_edit_employee_by_name(name):
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


    def delete_multiple_employees(self):
        self.events.is_element_displayed((By.XPATH, "//div[@class='oxd-table-body']/div"))
        rows = self.driver.find_elements(By.XPATH, "//div[@class='oxd-table-body']/div")
        selected_rows = random.sample(rows, 3)
        print("selected rows are ", selected_rows)
        employee_ids = []
        for row in selected_rows:
            self.events.click_element(element=row.find_element(By.XPATH, ".//div[@role='cell'][1]//input[@type='checkbox']"))
            #self.events.click_element((By.XPATH, ".//div[@role='cell'][1]//input[@type='checkbox']"))
            employee_ids.append(row.find_element(By.XPATH, ".//div[@role='cell'][2]").text)
        self.events.click_element((By.XPATH, "//button[.=' Delete Selected ']"))
        assert self.is_error_displayed(message="The selected record will be permanently deleted. Are you sure you want to continue?")
        self.events.click_element((By.XPATH, "//button[.=' Yes, Delete ']"))
        self.events.is_element_displayed((By.XPATH, "//div[@class='oxd-table-body']/div"))

        return employee_ids

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
        self.click_edit_employee_by_name(name)
        self.events.click_element((By.XPATH, "//a[text()='Contact Details']"))
        time.sleep(10)
        street1 = self.events.get_element_attribute((By.XPATH, "//label[text()='Street 1']/../following-sibling::div/input"), "value")
        city = self.events.get_element_attribute((By.XPATH, "//label[text()='City']/../following-sibling::div/input"), "value")
        mobile = self.events.get_element_attribute((By.XPATH, "//label[text()='Mobile']/../following-sibling::div/input"), "value")
        email = self.events.get_element_attribute((By.XPATH, "//label[text()='Work Email']/../following-sibling::div/input"), "value")
        print("details updated are :", street1, city, mobile, email)


    def is_personal_details_updated(self, name, dob, gender):
        self.click_edit_employee_by_name(name)
        time.sleep(10)
        dob_value = self.events.get_element_attribute((By.XPATH, f"//label[text()='Date of Birth']/../following-sibling::div//input[@placeholder='yyyy-dd-mm']"), "value")
        assert dob == dob_value, f"Expected DOB: {dob}, but got: {dob_value}"
        gender_xpath = f"//label[text()='{gender}']/input"
        is_selected = self.driver.find_element(By.XPATH, gender_xpath).is_selected()
        print(is_selected)
        assert is_selected == True, "Gender was not edited."


    def is_error_displayed(self, locator=None,  message="" ):
        if locator is None and message:
            locator = (By.XPATH, f"//*[text()='{message}']")
        elif locator is None:
            locator = self._ERROR_MSG

        return self._validators.validate_text_present(locator, message)

    def delete_employee(self, employee_id):
        self.events.click_element((By.XPATH, f"//div[@class='oxd-table-cell oxd-padding-cell']//div[text()='{employee_id}']/../following-sibling::div//i[contains(@class,'trash')]/parent::button"))
        assert self.is_error_displayed(message="The selected record will be permanently deleted. Are you sure you want to continue?")
        self.events.click_element(self._DELETE_CONFIRM_BUTTON)
        time.sleep(10)

    def check_employee_deleted(self, emp_id):
        self.events.enter_text(self._EMPLOYEE_ID_INPUT, emp_id)
        self.events.click_element(self._SEARCH_BUTTON)
        time.sleep(10)
        return len(self.get_employee_list())==0
