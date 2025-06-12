import pytest
from pages.pim import PIMPage
from pages.common_pages import HomePage
from selenium.webdriver.common.by import By
from utils.GenericUtils import *

@pytest.fixture(autouse=True)
def go_to_pim(selenium_driver):
    homePage = HomePage(selenium_driver)
    homePage.navigate_to_pim()
      # Ensure this navigates to the PIM section before each test

@pytest.mark.add_employee
@pytest.mark.smoke
def test_pim_001_create_employee(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="John", last_name="Doe", employee_id="1001")
    HomePage(selenium_driver).navigate_to_pim()
    assert pim.is_employee_present("John", "Doe", "1001")

@pytest.mark.regression
@pytest.mark.add_employee
@pytest.mark.negative
def test_pim_002_create_employee_blank_first_name(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="", last_name="Smith", employee_id="1003")
    assert pim.is_error_displayed(locator=(By.XPATH,"//input[@name='firstName']/../following-sibling::span[contains"
                                                    "(@class,'oxd-input-field-error-message')]"), message="Required")

@pytest.mark.regression
@pytest.mark.add_employee
@pytest.mark.negative
def test_pim_003_create_employee_blank_last_name(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Anna", last_name="", employee_id="1004")
    assert pim.is_error_displayed(locator=(By.XPATH, "//input[@name='lastName']/../following-sibling::span[contains"
                                                     "(@class,'oxd-input-field-error-message')]"), message="Required")
@pytest.mark.regression
@pytest.mark.add_employee
@pytest.mark.negative
def test_pim_004_create_employee_duplicate_emp_id(selenium_driver):
    pim = PIMPage(selenium_driver)
    emp_id = generate_unique_id()
    pim.add_employee(first_name="John", last_name="Doe", employee_id=emp_id)
    HomePage(selenium_driver).navigate_to_pim()
    pim.add_employee(first_name="John", last_name="Doe", employee_id=emp_id)
    assert pim.is_error_displayed(message="Employee Id already exists")

@pytest.mark.regression
@pytest.mark.add_employee
@pytest.mark.negative
def test_pim_005_create_employee_invalid_em_id(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Robert", last_name="Brown", employee_id="dsahdsjkahdksdsa")
    assert pim.is_error_displayed(message = "Should not exceed 10 characters")

@pytest.mark.regression
@pytest.mark.add_employee
@pytest.mark.negative
def test_pim_006__create_employee_invalid_first_name(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="VeryLongFirstNameExceedingLimit", last_name="Smith", employee_id="1006")
    assert pim.is_error_displayed("Should not exceed 30 characters")

@pytest.mark.edit_employee
@pytest.mark.regression
@pytest.mark.edit
def test_pim_007_edit_employee_update_personal_details(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_personal_details(name="Ahmed Maged", dob="1990-01-01", gender="Male")
    HomePage(selenium_driver).navigate_to_pim()
    pim.is_personal_details_updated("Ahmed Maged", "1990-01-01", "Male")

@pytest.mark.edit_employee
@pytest.mark.regression
@pytest.mark.edit
@pytest.mark.negative
def test_pim_008_edit_personal_details_invalid_dob(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_personal_details(name="bala kumar", dob="notadate", gender="Male")
    assert pim.is_error_displayed(message="Should be a valid date in yyyy-dd-mm format")

@pytest.mark.edit_employee
@pytest.mark.regression
@pytest.mark.edit
@pytest.mark.negative
def test_pim_009_edit_employee_update_contact_details(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_contact_details(name="bala kumar", address="123 Main St", city="Metropolis", mobile="1234567890", email="jane.smith@email.com")
    HomePage(selenium_driver).navigate_to_pim()
    pim.is_contact_details_updated("bala kumar", "123 Main St", "Metropolis", "1234567890", "jane.smith@email.com")

@pytest.mark.edit_employee
@pytest.mark.regression
@pytest.mark.edit
@pytest.mark.negative
def test_pim_010_edit_contact_details_invalid_mobile_number(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_contact_details(name="Jane Smith", address="123 Main St", city="Metropolis", mobile="notanumber", email="jane.smith@email.com")
    pim.is_error_displayed(message="Allows numbers and only + - / ( )")

@pytest.mark.edit_employee
@pytest.mark.regression
@pytest.mark.edit
@pytest.mark.negative
def test_pim_011_edit_contact_details_invalid_email(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_contact_details(name="Jane Smith", address="123 Main St", city="Metropolis", mobile="1234567890", email="invalidemail")
    assert pim.is_error_displayed(message="Expected format: admin@example.com")


@pytest.mark.delete_employee
@pytest.mark.smoke
@pytest.mark.delete
def test_pim_012_delete_single_employee(selenium_driver):
    pim = PIMPage(selenium_driver)
    emp_id = "0360"
    pim.delete_employee(emp_id)
    assert pim.check_employee_deleted(emp_id)

@pytest.mark.delete_employee
@pytest.mark.regression
@pytest.mark.delete
def test_pim_013_delete_multiple_employees(selenium_driver):
    pim = PIMPage(selenium_driver)
    emp_ids = pim.delete_multiple_employees()
    for emp_id in emp_ids:
        assert pim.check_employee_deleted(emp_id), f"Employee ID {emp_id} was not deleted!"
