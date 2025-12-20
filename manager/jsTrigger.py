import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
from concurrent.futures import ThreadPoolExecutor
import concurrent.futures
import time
from selenium_stealth import stealth

DEBUG_DIR = "/app/json"

def get_driver_path():
    system_driver = os.environ.get("CHROMEDRIVER_PATH")
    if system_driver:
        return system_driver
    return ChromeDriverManager().install()

def get_binary_location():
    return os.environ.get("CHROME_BIN")

try:
    DRIVER_PATH = get_driver_path()
except Exception as e:
    print(f"Error setting up driver: {e}")
    DRIVER_PATH = None

def handle_cookie_consent(driver):
    try:
        consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-primary-button, .fc-cta-consent"))
        )
        consent_button.click()
        time.sleep(1)
    except:
        pass

def save_debug_screenshot(driver, url):
    try:
        filename = "DEBUG_" + url.split('/')[-1] + ".png"
        filepath = os.path.join(DEBUG_DIR, filename)
        driver.save_screenshot(filepath)
    except:
        pass

def get_rendered_html(url, timeout=45):
    chrome_options = Options()
    
    chrome_bin = get_binary_location()
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--log-level=3")
        chrome_options.add_argument("start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)

    driver = None
    try:
        if not DRIVER_PATH:
            return url, "Error: Driver path not found"

        service = Service(executable_path=DRIVER_PATH)
        driver = webdriver.Chrome(service=service, options=chrome_options)

        stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

        driver.set_page_load_timeout(timeout)
        driver.get(url)
        
        # Obsługa Cookies
        handle_cookie_consent(driver)

        # Czekanie na dane
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "nethash"))
            )
        except TimeoutException:
            save_debug_screenshot(driver, url)
            return url, f"Error: Timeout waiting for #nethash on {url}"

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        
        return url, driver.page_source
        
    except Exception as e:
        return url, f"Error: {str(e)}"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass

def process_urls(urls, max_workers=2, timeout=60):
    results = {}
    safe_workers = min(max_workers, 2) 
    
    with ThreadPoolExecutor(max_workers=safe_workers) as executor:
        future_to_url = {
            executor.submit(get_rendered_html, url, timeout): url 
            for url in urls
        }
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                result_url, data = future.result(timeout=timeout + 10)
                results[result_url] = data
            except Exception as e:
                results[url] = f"Error: {str(e)}"
    
    return results