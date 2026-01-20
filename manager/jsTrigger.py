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

def create_driver():
    """Creates and returns a configured Chrome driver."""
    chrome_options = Options()
    chrome_bin = get_binary_location()
    if chrome_bin:
        chrome_options.binary_location = chrome_bin

    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage') 
    chrome_options.add_argument('--disable-gpu')
    
    chrome_options.add_argument('--disable-crash-reporter')
    chrome_options.add_argument('--disable-in-process-stack-traces')
    chrome_options.add_argument('--disable-logging')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument('--output=/dev/null')
    
    chrome_options.add_argument('--disable-software-rasterizer')
    chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument("--window-size=1920,1080")
    
    chrome_options.add_argument("start-maximized")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    if not DRIVER_PATH:
        raise Exception("Driver path not found")

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
    return driver

def handle_cookie_consent(driver):
    try:
        consent_button = WebDriverWait(driver, 3).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, ".fc-primary-button, .fc-cta-consent"))
        )
        consent_button.click()
        time.sleep(1)
    except:
        pass

def scrape_single_url(driver, url, timeout):
    try:
        driver.set_page_load_timeout(timeout)
        driver.get(url)
        
        handle_cookie_consent(driver)

        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.ID, "nethash"))
            )
        except TimeoutException:
            return url, f"Error: Timeout waiting for #nethash on {url}"

        driver.execute_script("window.scrollTo(0, 500);")
        time.sleep(1)
        return url, driver.page_source

    except Exception as e:
        return url, f"Error: {str(e)}"

def process_batch(urls, timeout):
    results = {}
    driver = None
    try:
        driver = create_driver()
        for url in urls:
            r_url, data = scrape_single_url(driver, url, timeout)
            results[r_url] = data
            
            time.sleep(2) 
            
    except Exception as e:
        print(f"Batch driver crashed: {e}")
        for url in urls:
            if url not in results:
                results[url] = f"Error: Driver crashed - {str(e)}"
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass
    return results

def process_urls(urls, max_workers=2, timeout=60):
    results = {}
    safe_workers = min(max_workers, 2)
    
    chunk_size = (len(urls) + safe_workers - 1) // safe_workers
    url_chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]
    
    with ThreadPoolExecutor(max_workers=safe_workers) as executor:
        futures = [
            executor.submit(process_batch, chunk, timeout) 
            for chunk in url_chunks
        ]
        
        for future in futures:
            try:
                batch_results = future.result()
                results.update(batch_results)
            except Exception as e:
                print(f"Worker exception: {e}")

    return results