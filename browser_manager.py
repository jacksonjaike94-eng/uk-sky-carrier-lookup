"""
Browser management and automation for UK Sky Carrier Lookup
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import config
from logger import log_info, log_error, log_warning, log_debug

class BrowserManager:
    def __init__(self):
        self.driver = None
        self.wait = None
        
    def initialize_browser(self):
        """Initialize Chrome browser with anti-detection settings"""
        try:
            log_info("Initializing browser...")
            
            chrome_options = Options()
            
            # Anti-detection measures
            if config.HEADLESS_MODE:
                chrome_options.add_argument("--headless=new")
            
            chrome_options.add_argument(f"--window-size={config.BROWSER_WINDOW_SIZE[0]},{config.BROWSER_WINDOW_SIZE[1]}")
            chrome_options.add_argument(f"user-agent={random.choice(config.USER_AGENTS)}")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            
            # Proxy support
            if config.PROXY:
                chrome_options.add_argument(f"--proxy-server={config.PROXY}")
                log_info(f"Using proxy: {config.PROXY}")
            
            # Initialize driver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.wait = WebDriverWait(self.driver, config.PAGE_LOAD_TIMEOUT)
            
            # Execute stealth script
            self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': 'Object.defineProperty(navigator, "webdriver", {get: () => false,});'
            })
            
            log_info("Browser initialized successfully")
            return True
            
        except Exception as e:
            log_error(f"Failed to initialize browser: {str(e)}")
            return False
    
    def navigate_to_url(self, url):
        """Navigate to target URL"""
        try:
            log_info(f"Navigating to: {url}")
            self.driver.get(url)
            time.sleep(random.uniform(2, 4))  # Random delay
            return True
        except Exception as e:
            log_error(f"Failed to navigate to {url}: {str(e)}")
            return False
    
    def find_element(self, by, value, timeout=None):
        """Find element with waiting"""
        try:
            if timeout is None:
                timeout = config.PAGE_LOAD_TIMEOUT
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(EC.presence_of_element_located((by, value)))
            return element
        except Exception as e:
            log_warning(f"Element not found: {by}={value}")
            return None
    
    def click_element(self, by, value):
        """Click element safely"""
        try:
            element = self.find_element(by, value)
            if element:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
                time.sleep(0.5)
                element.click()
                return True
            return False
        except Exception as e:
            log_error(f"Failed to click element: {str(e)}")
            return False
    
    def input_text(self, by, value, text):
        """Input text into element"""
        try:
            element = self.find_element(by, value)
            if element:
                element.clear()
                time.sleep(0.3)
                element.send_keys(text)
                return True
            return False
        except Exception as e:
            log_error(f"Failed to input text: {str(e)}")
            return False
    
    def get_page_source(self):
        """Get current page HTML"""
        try:
            return self.driver.page_source
        except Exception as e:
            log_error(f"Failed to get page source: {str(e)}")
            return None
    
    def check_for_captcha(self):
        """Check if CAPTCHA is present on page"""
        try:
            captcha_selectors = [
                "[data-sitekey]",
                ".g-recaptcha",
                "iframe[src*='recaptcha']",
                "[class*='captcha']"
            ]
            
            for selector in captcha_selectors:
                try:
                    self.driver.find_element(By.CSS_SELECTOR, selector)
                    log_warning("CAPTCHA detected on page!")
                    return True
                except:
                    continue
            
            return False
        except Exception as e:
            log_debug(f"Error checking for CAPTCHA: {str(e)}")
            return False
    
    def handle_captcha_manually(self):
        """Pause for manual CAPTCHA solving"""
        try:
            log_warning("CAPTCHA detected! Please solve it manually in the browser window...")
            log_info(f"Waiting {config.CAPTCHA_TIMEOUT} seconds for manual CAPTCHA solving...")
            
            for i in range(config.CAPTCHA_TIMEOUT):
                time.sleep(1)
                # Check if CAPTCHA is gone (element disappears)
                try:
                    self.driver.find_element(By.CSS_SELECTOR, "[data-sitekey]")
                except:
                    log_info("CAPTCHA solved successfully!")
                    return True
            
            log_error(f"CAPTCHA not solved within {config.CAPTCHA_TIMEOUT} seconds")
            return False
            
        except Exception as e:
            log_error(f"Error during CAPTCHA handling: {str(e)}")
            return False
    
    def close_browser(self):
        """Close browser"""
        try:
            if self.driver:
                self.driver.quit()
                log_info("Browser closed successfully")
        except Exception as e:
            log_error(f"Error closing browser: {str(e)}")