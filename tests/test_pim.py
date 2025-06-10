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

@pytest.mark.smoke
def test_TC_001(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="John", last_name="Doe", employee_id="1001")
    HomePage(selenium_driver).navigate_to_pim()
    assert pim.is_employee_present("John", "Doe", "1001")

@pytest.mark.smoke
def test_TC_002(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1002")
    HomePage(selenium_driver).navigate_to_pim()
    assert pim.is_employee_present("Jane", "Smith", "1002")

@pytest.mark.regression
def test_TC_003(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="", last_name="Smith", employee_id="1003")
    assert pim.is_error_displayed(locator=(By.XPATH,"//input[@name='firstName']/../following-sibling::span[contains"
                                                    "(@class,'oxd-input-field-error-message')]"), message="Required")
@pytest.mark.regression
def test_TC_004(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Anna", last_name="", employee_id="1004")
    assert pim.is_error_displayed(locator=(By.XPATH, "//input[@name='lastName']/../following-sibling::span[contains"
                                                     "(@class,'oxd-input-field-error-message')]"), message="Required")
@pytest.mark.negative
def test_TC_005(selenium_driver):
    pim = PIMPage(selenium_driver)
    emp_id = generate_unique_id()
    pim.add_employee(first_name="John", last_name="Doe", employee_id=emp_id)
    HomePage(selenium_driver).navigate_to_pim()
    pim.add_employee(first_name="John", last_name="Doe", employee_id=emp_id)
    assert pim.is_error_displayed("Employee Id is duplicated")

def test_TC_006(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.add_employee(first_name="Robert", last_name="Brown", employee_id="abcd")
    assert pim.is_error_dislayed("Invalid employee ID")

def test_TC_007(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Alice", last_name="Johnson", employee_id="1005")
    assert pim.is_employee_present("Alice", "Johnson", "1005")

def test_TC_008(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.add_employee(first_name="VeryLongFirstNameExceedingLimit", last_name="Smith", employee_id="1006")
    assert pim.is_error_displayed("First name exceeds character limit")

def test_TC_009(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1007")
    assert pim.is_employee_present("Jane", "Smith", "1007")

def test_TC_010(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.add_employee(first_name="Jane", last_name="Smith", employee_id="")
    assert pim.is_error_displayed("Employee ID is required")

def test_TC_011(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1008")
    assert pim.is_employee_present("Jane", "Smith", "1008")

def test_TC_012(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1009")
    assert pim.is_employee_present("Jane", "Smith", "1009")

def test_TC_013(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1010")
    assert pim.is_employee_present("Jane", "Smith", "1010")

def test_TC_014(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1011")
    assert pim.is_employee_present("Jane", "Smith", "1011")

def test_TC_015(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1012")
    assert pim.is_employee_present("Jane", "Smith", "1012")

def test_TC_016(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1013")
    assert pim.is_employee_present("Jane", "Smith", "1013")

def test_TC_017(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1014")
    assert pim.is_employee_present("Jane", "Smith", "1014")

def test_TC_018(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1015")
    assert pim.is_employee_present("Jane", "Smith", "1015")

def test_TC_019(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1016")
    assert pim.is_employee_present("Jane", "Smith", "1016")

def test_TC_020(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.add_employee(first_name="Jane", last_name="Smith", employee_id="1017")
    assert pim.is_employee_present("Jane", "Smith", "1017")

def test_TC_021(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_personal_details(name="John Doe", dob="1990-01-01", gender="Male")
    assert pim.is_personal_details_updated("John Doe", "1990-01-01", "Male")

def test_TC_022(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_personal_details(name="John Doe", dob="notadate", gender="Male")
    assert pim.is_error_displayed("Invalid date of birth")

def test_TC_023(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_personal_details(name="John Doe", dob="1990-01-01", gender="Unknown")
    assert pim.is_error_displayed("Invalid gender")

def test_TC_024(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_contact_details(name="Jane Smith", address="123 Main St", city="Metropolis", mobile="1234567890", email="jane.smith@email.com")
    assert pim.is_contact_details_updated("Jane Smith", "123 Main St", "Metropolis", "1234567890", "jane.smith@email.com")

def test_TC_025(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_contact_details(name="Jane Smith", address="", city="Metropolis", mobile="1234567890", email="jane.smith@email.com")
    assert pim.is_error_displayed("Address is required")

def test_TC_026(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_contact_details(name="Jane Smith", address="123 Main St", city="Metropolis", mobile="notanumber", email="jane.smith@email.com")
    assert pim.is_error_displayed("Invalid mobile number")

def test_TC_027(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_contact_details(name="Jane Smith", address="123 Main St", city="Metropolis", mobile="1234567890", email="invalidemail")
    assert pim.is_error_displayed("Invalid email address")

def test_TC_028(selenium_driver):
    pim = PIMPage(selenium_driver)
    pim.edit_experience_details(name="Alice Johnson", company="Acme Corp", job_title="Engineer", from_date="2015-01-01", to_date="2020-01-01")
    assert pim.is_experience_details_updated("Alice Johnson", "Acme Corp", "Engineer", "2015-01-01", "2020-01-01")

def test_TC_029(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_experience_details(name="Alice Johnson", company="Acme Corp", job_title="Engineer", from_date="2020-01-01", to_date="2015-01-01")
    assert pim.is_error_displayed("From date must be before to date")

def test_TC_030(selenium_driver):
    pim = PIMPage(selenium_driver)
    with pytest.raises(Exception):
        pim.edit_personal_details(name="Nonexistent User", dob="1990-01-01", gender="Male")
    assert pim.is_error_displayed("User not found")
# ...repeat for other test cases, each will start from the PIM page