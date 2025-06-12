import time

import pytest
from pages.recruitment import RecruitmentPage
from pages.common_pages import HomePage
from selenium.webdriver.common.by import By
from utils.GenericUtils import *


@pytest.fixture(autouse=True)
def go_to_recruitment(selenium_driver):
    homePage = HomePage(selenium_driver)
    homePage.navigate_to_recruitment()

@pytest.mark.recruitment
@pytest.mark.add_candidate
@pytest.mark.smoke
def test_recruitment_001_add_candidate(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    first_name = generate_unique_string(length=5)
    last_name = generate_unique_string(length=6)

    recruitment.add_candidate(first_name=first_name, last_name=last_name, email="alice.smith@email.com")
    time.sleep(10)
    HomePage(selenium_driver).navigate_to_recruitment()
    time.sleep(10)
    print("nagivated to recruitment page")
    assert recruitment.is_candidate_present(first_name+" " + last_name)

@pytest.mark.recruitment
@pytest.mark.regression
@pytest.mark.add_candidate
@pytest.mark.negative
def test_recruitment_002_add_candidate_blank_first_name(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    recruitment.add_candidate(first_name="", last_name="Brown", email="brown@email.com")
    assert recruitment.is_error_displayed(locator=(By.XPATH, "//input[@name='firstName']/../following-sibling::span"), message="Required")

@pytest.mark.recruitment
@pytest.mark.regression
@pytest.mark.add_candidate
@pytest.mark.negative
def test_recruitment_003_add_candidate_blank_last_name(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    recruitment.add_candidate(first_name="Bob", last_name="", email="bob@email.com")
    assert recruitment.is_error_displayed(locator=(By.XPATH, "//input[@name='lastName']/../following-sibling::span"), message="Required")

@pytest.mark.recruitment
@pytest.mark.regression
@pytest.mark.add_candidate
@pytest.mark.negative
def test_recruitment_004_add_candidate_invalid_email(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    recruitment.add_candidate(first_name="Carol", last_name="White", email="invalidemail")
    assert recruitment.is_error_displayed(message="Expected format: admin@example.com")

@pytest.mark.recruitment
@pytest.mark.edit_candidate
@pytest.mark.regression
@pytest.mark.edit
def test_recruitment_006_edit_candidate_update_details(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    recruitment.edit_candidate(name="Alice Smith", new_details={"first_name": "Alicia", "email": "alicia.smith@email.com"})
    HomePage(selenium_driver).navigate_to_recruitment()
    assert recruitment.is_candidate_present("Alicia", "Smith", "alicia.smith@email.com")

@pytest.mark.recruitment
@pytest.mark.edit_candidate
@pytest.mark.regression
@pytest.mark.edit
@pytest.mark.negative
def test_recruitment_007_edit_candidate_invalid_email(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    recruitment.edit_candidate(name="Alicia Smith", new_details={"email": "notanemail"})
    assert recruitment.is_error_displayed(locator=(By.NAME, "email"), message="Expected format: admin@example.com")

@pytest.mark.recruitment
@pytest.mark.delete_candidate
@pytest.mark.smoke
@pytest.mark.delete
def test_recruitment_008_delete_single_candidate(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    candidate_name = "Charles Haywire"
    recruitment.delete_candidate(candidate_name)
    assert recruitment.check_candidate_deleted(candidate_name)

@pytest.mark.recruitment
@pytest.mark.delete_candidate1
@pytest.mark.regression
@pytest.mark.delete
def test_recruitment_009_delete_multiple_candidates(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    candidate_names = recruitment.delete_multiple_candidates()
    for name in candidate_names:
        assert recruitment.check_candidate_deleted(name), f"Candidate {name} was not deleted!"

@pytest.mark.recruitment
@pytest.mark.regression
@pytest.mark.search_candidate
def test_recruitment_010_search_candidate_by_name(selenium_driver):
    recruitment = RecruitmentPage(selenium_driver)
    candidates = recruitment.search_candidate(name="Alicia")
    assert any("Alicia" in c[0] for c in candidates)

