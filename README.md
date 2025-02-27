# Germany Hospital Scraper

## Description

This project is a Python-based web scraper designed to collect data on hospitals in Germany from the Deutsches Krankenhaus Verzeichnis website. The script uses **Selenium** to navigate the website and extract hospital details such as names, phone numbers, email addresses, and websites.

## Features

- Scrapes hospital data for all **16 German Bundesländer**.
- Extracts hospital **name, phone number, email, and website**.
- Handles obfuscated email addresses by reversing them.
- Uses **gender detection** to infer the appropriate salutation for hospital contacts.
- Saves the collected data into a structured CSV file.

## Requirements

To run this script, ensure you have the following installed:

- Python 3.x
- Selenium
- WebDriver Manager
- pandas
- gender-guesser

You can install the required dependencies using:

```sh
pip install selenium webdriver-manager pandas gender-guesser
```

## Usage

1. Clone this repository:

```sh
git clone https://github.com/PeppiDufter/hospital-scraper.git
cd hospital-scraper
```

2. Run the script:

```sh
python germany_hospital_scraper.py
```

3. The script will create a CSV file `german_hospitals.csv` with the scraped data.

## How It Works

- Initializes a **headless Selenium WebDriver**.
- Iterates through each German state to extract hospital lists.
- Visits each hospital's detail page to extract contact information.
- Cleans and processes the data before saving it to CSV.

## Output Format

The extracted hospital data is saved in `german_hospitals.csv` with the following columns:

- `Hospital Name`
- `Phone`
- `Email`
- `Website`
- `Anrede` (Salutation based on gender detection)

## Contributing

Feel free to submit issues or fork this repository and submit pull requests for improvements.

## License

This project is licensed under the MIT License.

