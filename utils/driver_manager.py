import json
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from appium import webdriver as appium_webdriver


class DriverManager:
    def __init__(self, config_path):
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

        try:
            with open(config_path) as f:
                self.config = json.load(f)
            self.logger.info("Configuration file loaded successfully.")
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_path}")
            raise
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON format in configuration file: {config_path}")
            raise
        self.driver = None

    def launch_application(self):
        try:
            browser = self.config.get("browser", "chrome").lower()
            env_url = self.config.get("environments", {}).get(self.config.get("environment", "dev")).get("url","")
            print(env_url)
            #print("url is " + env_url)

            is_mobile = self.config.get("mobile", False)

            if is_mobile:
                self.logger.info("Initializing mobile driver.")
                self.driver = self._init_mobile_driver()
            else:
                self.logger.info(f"Initializing web driver for browser: {browser}.")
                self.driver = self._init_web_driver(browser)

            self.driver.maximize_window()
            self.logger.info("Browser window maximized.")

            if env_url:
                self.logger.info(f"Navigating to URL: {env_url}.")
                self.driver.get(env_url)
            else:
                self.logger.error("Environment URL is not specified in the configuration.")
                raise ValueError("Environment URL is not specified in the configuration.")

            return self.driver
        except WebDriverException as e:
            self.logger.error(f"Failed to launch the application: {e}")
            raise

    def _init_web_driver(self, browser):
        try:
            if browser == "chrome":
                return webdriver.Chrome(service=ChromeService())
            elif browser == "firefox":
                return webdriver.Firefox(service=FirefoxService())
            elif browser == "edge":
                return webdriver.Edge(service=EdgeService())
            elif browser == "remote":
                remote_url = self.config.get("remote_url")
                capabilities = self.config.get("capabilities", DesiredCapabilities.CHROME.copy())
                return webdriver.Remote(command_executor=remote_url, desired_capabilities=capabilities)
            else:
                self.logger.error(f"Unsupported browser: {browser}")
                raise ValueError(f"Unsupported browser: {browser}")
        except WebDriverException as e:
            self.logger.error(f"Error initializing WebDriver for browser '{browser}': {e}")
            raise

    def _init_mobile_driver(self):
        try:
            remote_url = self.config.get("appium_server_url")
            desired_caps = self.config.get("desired_capabilities", {})
            return appium_webdriver.Remote(command_executor=remote_url, desired_capabilities=desired_caps)
        except Exception as e:
            self.logger.error(f"Error initializing mobile driver: {e}")
            raise

    def switch_to_window(self, index=0):
        try:
            handles = self.driver.window_handles
            if index < len(handles):
                self.logger.info(f"Switching to window with index: {index}.")
                self.driver.switch_to.window(handles[index])
            else:
                self.logger.error(f"Window index {index} is out of range.")
                raise IndexError(f"Window index {index} is out of range.")
        except Exception as e:
            self.logger.error(f"Error switching to window: {e}")
            raise

    def switch_to_frame(self, locator):
        try:
            self.logger.info(f"Switching to frame with locator: {locator}.")
            frame = self.driver.find_element(*locator)
            self.driver.switch_to.frame(frame)
        except Exception as e:
            self.logger.error(f"Error switching to frame: {e}")
            raise

    def switch_to_default_content(self):
        try:
            self.logger.info("Switching to default content.")
            self.driver.switch_to.default_content()
        except Exception as e:
            self.logger.error(f"Error switching to default content: {e}")
            raise

    def close(self):
        try:
            self.logger.info("Closing the current browser window.")
            self.driver.close()
        except Exception as e:
            self.logger.error(f"Error closing the driver: {e}")
            raise

    def quit(self):
        try:
            self.logger.info("Quitting the browser driver.")
            self.driver.quit()
        except Exception as e:
            self.logger.error(f"Error quitting the driver: {e}")
            raise