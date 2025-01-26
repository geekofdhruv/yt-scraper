import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to set up the WebDriver
def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # Open browser maximized
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

# Function to scrape YouTube channel data
def scrape_youtube_channel(url):
    try:
        # Initialize WebDriver
        driver = setup_driver()

        # Open the provided URL
        print(f"Opening URL: {url}")
        driver.get(url)

        # Wait for elements to load dynamically
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@role='text' and @dir='auto']")))

        # Locate elements using XPath
        xpath = "//span[@role='text' and @dir='auto']"
        elements = driver.find_elements(By.XPATH, xpath)

        # Parse required information
        channel_name = elements[0].text if len(elements) > 0 else None
        username = elements[1].text if len(elements) > 1 else None
        subscribers = elements[2].text if len(elements) > 2 else None
        videos = elements[3].text if len(elements) > 3 else None

        # Collect data into a dictionary
        channel_info = {
            'channel_name': channel_name,
            'username': username,
            'subscribers': subscribers,
            'no_of_videos': videos
        }

        print("\nScraped Channel Information:")
        print(channel_info)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Quit the WebDriver
        driver.quit()

# Main function
if __name__ == "__main__":
    # Take URL input from the user
    url = input("Enter the YouTube Channel URL: ").strip()

    # Run the scraper with the provided URL
    scrape_youtube_channel(url)
