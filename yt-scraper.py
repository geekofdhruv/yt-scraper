from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def setup_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")  # Open browser maximized
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    service = ChromeService(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)


def scrape_youtube_channel(url):
    try:

        driver = setup_driver()

        print(f"Opening URL: {url}")
        driver.get(url)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.XPATH, "//span[@role='text' and @dir='auto']")))

        xpath = "//span[@role='text' and @dir='auto']"
        elements = driver.find_elements(By.XPATH, xpath)

        channel_name = elements[0].text if len(elements) > 0 else None
        username = elements[1].text if len(elements) > 1 else None
        subscribers = elements[2].text if len(elements) > 2 else None
        videos = elements[3].text if len(elements) > 3 else None

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
        driver.quit()


if __name__ == "__main__":
    url = input("Enter the YouTube Channel URL: ").strip()
    scrape_youtube_channel(url)