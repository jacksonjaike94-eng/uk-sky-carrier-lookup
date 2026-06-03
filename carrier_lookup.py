"""
Carrier lookup logic for freecarrierlookup.com
"""

import time
import random
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import config
from browser_manager import BrowserManager
from logger import log_info, log_error, log_warning

class CarrierLookup:
    def __init__(self):
        self.browser = BrowserManager()
        self.results = []
        
    def start(self):
        """Initialize browser"""
        return self.browser.initialize_browser()
    
    def lookup_number(self, phone_number):
        """Lookup single phone number"""
        try:
            log_info(f"Looking up: {phone_number}")
            
            # Navigate to website
            if not self.browser.navigate_to_url(config.TARGET_URL):
                return {"phone": phone_number, "carrier": None, "status": "error_navigate"}
            
            # Find input field
            input_selectors = [
                "input[placeholder*='phone']",
                "input[type='text']",
                "input[id*='phone']",
                "input[class*='phone']"
            ]
            
            input_found = False
            for selector in input_selectors:
                if self.browser.input_text(By.CSS_SELECTOR, selector, phone_number):
                    input_found = True
                    log_info(f"Entered number in input field")
                    break
            
            if not input_found:
                log_error(f"Could not find input field for {phone_number}")
                return {"phone": phone_number, "carrier": None, "status": "error_input"}
            
            # Wait before submitting
            time.sleep(random.uniform(1, 3))
            
            # Find and click submit button
            submit_selectors = [
                "button[type='submit']",
                "button[id*='search']",
                "button[class*='submit']",
                "button"
            ]
            
            submit_found = False
            for selector in submit_selectors:
                if self.browser.click_element(By.CSS_SELECTOR, selector):
                    submit_found = True
                    log_info("Clicked submit button")
                    break
            
            if not submit_found:
                # Try using Enter key
                input_element = self.browser.find_element(By.CSS_SELECTOR, "input[type='text']")
                if input_element:
                    input_element.submit()
                    log_info("Submitted form with Enter key")
                else:
                    log_error(f"Could not submit form for {phone_number}")
                    return {"phone": phone_number, "carrier": None, "status": "error_submit"}
            
            # Wait for results
            time.sleep(random.uniform(3, 6))
            
            # Check for CAPTCHA
            if self.browser.check_for_captcha():
                log_warning(f"CAPTCHA detected for {phone_number}")
                if self.browser.handle_captcha_manually():
                    time.sleep(random.uniform(2, 4))
                else:
                    return {"phone": phone_number, "carrier": None, "status": "error_captcha"}
            
            # Get results
            page_source = self.browser.get_page_source()
            if not page_source:
                return {"phone": phone_number, "carrier": None, "status": "error_page_source"}
            
            # Parse results
            carrier = self.parse_carrier_from_page(page_source)
            
            if carrier:
                log_info(f"Found carrier: {carrier}")
                
                # Check if it's Sky UK Limited
                if config.ENABLED_FILTERING:
                    if carrier.lower() == config.TARGET_CARRIER.lower():
                        return {"phone": phone_number, "carrier": carrier, "status": "success"}
                    else:
                        return {"phone": phone_number, "carrier": carrier, "status": "filtered"}
                else:
                    return {"phone": phone_number, "carrier": carrier, "status": "success"}
            else:
                log_warning(f"Could not extract carrier for {phone_number}")
                return {"phone": phone_number, "carrier": None, "status": "error_parsing"}
            
        except Exception as e:
            log_error(f"Error looking up {phone_number}: {str(e)}")
            return {"phone": phone_number, "carrier": None, "status": "error_exception"}
        
        finally:
            # Add delay before next request
            time.sleep(config.DELAY_BETWEEN_REQUESTS + random.uniform(1, 3))
    
    def parse_carrier_from_page(self, html):
        """Extract carrier information from page HTML"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # Look for common carrier display patterns
            result_divs = soup.find_all(['div', 'span', 'p'])
            
            for div in result_divs:
                text = div.get_text(strip=True)
                # Look for carrier name patterns
                if any(keyword in text.lower() for keyword in ['sky', 'vodafone', 'o2', 'three', 'virgin', 'bt', 'ee']):
                    # Extract carrier name
                    if 'Sky' in text or 'sky' in text:
                        return "Sky UK Limited"
                    elif 'Vodafone' in text or 'vodafone' in text:
                        return "Vodafone"
                    elif 'O2' in text or 'o2' in text:
                        return "O2"
                    elif 'Three' in text or 'three' in text:
                        return "Three"
                    elif 'Virgin' in text or 'virgin' in text:
                        return "Virgin Media"
                    elif 'BT' in text or 'bt' in text:
                        return "BT"
                    elif 'EE' in text or 'ee' in text:
                        return "EE"
            
            # Try alternative parsing
            text = soup.get_text()
            if 'Sky UK Limited' in text:
                return "Sky UK Limited"
            elif 'Sky' in text:
                return "Sky UK Limited"
            
            return None
            
        except Exception as e:
            log_error(f"Error parsing carrier from page: {str(e)}")
            return None
    
    def process_file(self, input_file):
        """Process numbers from file"""
        try:
            log_info(f"Reading numbers from {input_file}")
            
            numbers = []
            with open(input_file, 'r') as f:
                for line in f:
                    number = line.strip()
                    if number:
                        numbers.append(number)
            
            log_info(f"Found {len(numbers)} numbers to process")
            
            # Process each number
            for i, number in enumerate(numbers, 1):
                log_info(f"Processing {i}/{len(numbers)}: {number}")
                result = self.lookup_number(number)
                self.results.append(result)
            
            return self.results
            
        except FileNotFoundError:
            log_error(f"Input file not found: {input_file}")
            return None
        except Exception as e:
            log_error(f"Error processing file: {str(e)}")
            return None
    
    def close(self):
        """Close browser"""
        self.browser.close_browser()