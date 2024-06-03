import os
import re
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def validate_url(url):
    return bool(re.match(r'https?://www\.linkedin\.com/in/[a-zA-Z0-9\-_]+/?$', url))

def login(driver):
    try:
        email = input("Enter your LinkedIn email: ").strip()
        password = input("Enter your LinkedIn password: ").strip()

        if not email or not password:
            print("LinkedIn email or password not provided.")
            return False

        print("Navigating to LinkedIn login page...")
        driver.get("https://www.linkedin.com/login")
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "username")))

        print("Entering email...")
        email_field = driver.find_element(By.ID, "username")
        email_field.send_keys(email)

        print("Entering password...")
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys(password)

        print("Clicking login button...")
        login_button = driver.find_element(By.XPATH, '//*[@id="organic-div"]/form/div[3]/button')
        login_button.click()

        print("Waiting for navigation to complete...")
        WebDriverWait(driver, 90).until(EC.presence_of_element_located((By.XPATH, '//*[@id="global-nav"]')))

        # Check if a new tab has been opened and switch to it
        if len(driver.window_handles) > 1:
            driver.switch_to.window(driver.window_handles[1])
        
        print("Login successful!")
        return True

    except Exception as e:
        print(f"Error during login: {e}")
        return False

def scroll_page(driver):
    try:
        print("Scrolling the page...")
        # Scroll down to the bottom of the page to load dynamic content
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Add a delay after scrolling
        print("Scrolling complete.")
    except Exception as e:
        print(f"Error scrolling the page: {e}")

def click_see_more_buttons(driver):
    print("Clicking 'See more' buttons...")
    try:
        while True:
            see_more_buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'pv-profile-section__see-more-inline')]")
            if not see_more_buttons:
                break
            for button in see_more_buttons:
                try:
                    driver.execute_script("arguments[0].click();", button)
                    time.sleep(2)
                except Exception as e:
                    print(f"Error clicking a 'See more' button: {e}")
    except Exception as e:
        print(f"Error clicking 'See more' buttons: {e}")

def scrape_experience(driver, url):
    try:
        print(f"Navigating to {url}...")
        driver.get(url)
        
        WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        scroll_page(driver)
        click_see_more_buttons(driver)

        print("Fetching page source...")
        page_source = driver.page_source

        # Debugging: Output page source to check for the experience section
        with open('page_source.html', 'w', encoding='utf-8') as file:
            file.write(page_source)
        print("Page source saved for debugging.")

        soup = BeautifulSoup(page_source, 'html.parser')

        print("Searching for experience section...")
        experience_section = soup.find('section', {'id': 'experience-section'})
        if not experience_section:
            experience_section = soup.find('section', class_='experience-section')
        if not experience_section:
            experience_section = soup.find('section', {'aria-label': 'Experience'})
        if not experience_section:
            print("No experience section found.")
            return []

        experiences = experience_section.find_all('li', recursive=False)
        if not experiences:
            print("No experience data found.")
            return []

        print("Extracting experience data...")
        experience_list = []
        for exp in experiences:
            try:
                title = exp.find('h3').get_text().strip() if exp.find('h3') else 'N/A'
                company_name = exp.find('p', class_='pv-entity__secondary-title').get_text().strip() if exp.find('p', class_='pv-entity__secondary-title') else 'N/A'
                date_range = exp.find('h4', class_='pv-entity__date-range').find_all('span')[1].get_text().strip() if exp.find('h4', class_='pv-entity__date-range') else 'N/A'
                location = exp.find('h4', class_='pv-entity__location').find_all('span')[1].get_text().strip() if exp.find('h4', class_='pv-entity__location') else 'N/A'
                responsibilities = exp.find('ul', class_='pv-entity__description-list').find_all('li') if exp.find('ul', class_='pv-entity__description-list') else []
                responsibilities_text = ', '.join([resp.get_text().strip() for resp in responsibilities])
                
                experience_data = {
                    'Role': title,
                    'Company': company_name,
                    'Duration': date_range,
                    'Location': location,
                    'Work Responsibilities': responsibilities_text
                }
                experience_list.append(experience_data)
            except Exception as e:
                print(f"Error extracting data for an experience: {e}")

        return experience_list

    except Exception as e:
        print(f"Error during scraping: {e}")
        import traceback
        traceback.print_exc()  # Print traceback for detailed error analysis
        return []

def save_to_csv(data):
    try:
        df = pd.DataFrame(data)
        df.to_csv('linkedin_experience.csv', index=False)
        print("Data saved to linkedin_experience.csv")
    except Exception as e:
        print(f"Error saving data to CSV: {e}")

def main():
    service = Service("F:\Project\chromedriver.exe")  ## add path for the chrome driver
    driver = webdriver.Chrome(service=service)

    try:
        if not login(driver):
            return

        profile_url = input("Enter the LinkedIn profile URL: ")
        if validate_url(profile_url):
            experience_data = scrape_experience(driver, profile_url)
            if experience_data:
                save_to_csv(experience_data)
            else:
                print("No experience data found.")
        else:
            print("Invalid URL. Please enter a valid LinkedIn profile URL.")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
