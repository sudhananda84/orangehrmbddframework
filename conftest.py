import pytest
from utils.driver_manager import DriverManager
from pages.common_pages import LoginPage

@pytest.fixture(scope="session")
def driver_manager():
    # Adjust the config path as needed
    return DriverManager('config.json')

@pytest.fixture(scope="session")
def selenium_driver(driver_manager):
    driver = driver_manager.launch_application()
    # Get credentials from config
    config = driver_manager.config
    env = config.get("environment", "dev")
    env_config = config.get("environments", {}).get(env, {})
    username = env_config.get("username")
    password = env_config.get("password")
    # Perform login
    login_page = LoginPage(driver)
    login_page.login_valid(username, password)
    yield driver
    driver_manager.quit()