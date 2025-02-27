import os
import time
import pandas as pd
import re
import urllib.parse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from gender_guesser.detector import Detector

# Set up Selenium WebDriver options
def init_driver():
    """Initialize and configure the Selenium WebDriver."""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=chrome_options)

def scrape_hospital_list(driver, region):
    """Scrape a list of hospitals for a given region."""
    base_url = "https://www.deutsches-krankenhaus-verzeichnis.de/app/suche/bundesland/"
    driver.get(base_url + region)
    time.sleep(2)  # Allow page to load
    
    try:
        locations = driver.execute_script("return locations;")
        return pd.DataFrame([{ "name": h["name"], "path": h["path"]} for h in locations])
    except Exception:
        return pd.DataFrame()

def scrape_hospital_data(driver, hospital):
    """Scrape detailed information for a single hospital."""
    base_url = "https://www.deutsches-krankenhaus-verzeichnis.de"
    driver.get(base_url + hospital["path"])
    wait = WebDriverWait(driver, 2)

    def get_text(xpath):
        """Extract text content from a given XPath."""
        try:
            return wait.until(EC.presence_of_element_located((By.XPATH, xpath))).text.strip()
        except:
            return "Not found"

    return {
        "Hospital Name": hospital["name"],
        "Phone": get_text("//a[contains(@href, 'tel:')]"),
        "Email": get_text("//a[contains(@href, 'mailto:')]"),
        "Website": get_text("//a[contains(@class, 'url') and @href]"),
    }

def clean_and_transform(df):
    """Clean and transform hospital data by processing names, emails, and gender information."""
    detector = Detector(case_sensitive=False)
    
    def flip_email(email):
        """Reverse email string to fix obfuscation."""
        return email[::-1] if isinstance(email, str) else email
    
    def clean_name(name):
        """Remove common titles and extract the first name."""
        if not isinstance(name, str):
            return "unknown"
        return re.sub(r'(Dr.|Prof.|Dipl.|MBA|PhD|BSc|MSc)', '', name).strip().split()[0]
    
    def guess_gender(name):
        """Guess gender based on first name."""
        gender = detector.get_gender(clean_name(name))
        return "Herr" if gender in ["male", "mostly_male"] else "Frau" if gender in ["female", "mostly_female"] else "Damen und Herren"
    
    df["Email"] = df["Email"].apply(flip_email)
    df["Anrede"] = df["Hospital Name"].apply(guess_gender)
    return df

def main():
    """Main function to orchestrate the scraping and data processing."""
    bundeslaender = [
        "bremen", "hamburg", "berlin", "bayern", "baden-wuerttemberg", "saarland", "rheinland-pfalz", "hessen", "thueringen",
        "sachsen", "brandenburg", "sachsen-anhalt", "niedersachsen", "nordrhein-westfalen", "schleswig-holstein", "mecklenburg-vorpommern"
    ]
    
    driver = init_driver()
    all_hospitals = []
    
    for region in bundeslaender:
        print(f"Scraping {region}...")
        hospital_list = scrape_hospital_list(driver, region)
        all_hospitals.extend([scrape_hospital_data(driver, row) for _, row in hospital_list.iterrows()])
    
    driver.quit()
    
    df = pd.DataFrame(all_hospitals)
    df = clean_and_transform(df)
    df.to_csv("german_hospitals.csv", index=False)
    print("Data saved to german_hospitals.csv")

if __name__ == "__main__":
    main()
