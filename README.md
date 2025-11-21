# 🚗 Wallapop & Autocasion Data Scraper

A powerful web scraping tool built with **Python** and **Selenium** to analyze the second-hand car market in Spain.

## 🎯 Objective
To extract real-time pricing, mileage, year, and horsepower data from major marketplaces (Wallapop, Autocasion) to build a dataset for Data Science analysis.

## ⚙️ Key Features
- **Dynamic Navigation:** Uses `Selenium` to handle cookies, pop-ups, and dynamic loading.
- **Multi-Brand Support:** Automatically searches for specific models (Audi, BMW, Porsche).
- **Data Cleaning:** Extracts raw HTML and converts it into structured data.
- **CSV Export:** automatically generates structured `.csv` datasets ready for analysis.

## 🛠️ Technologies Used
- **Python 3**
- **Selenium** (Browser Automation & Navigation)
- **CSV Module** (Native Data Structuring & Export)
- **Webdriver Manager** (Chrome Driver handling)

## 🚀 How to run
1. Install requirements:
        pip install selenium webdriver-manager

2. Run the script:
        python scraper.py

3. The script will open Chrome, navigate automatically, and save the data into `.csv` files.

---
*Disclaimer: This tool is for educational purposes only.*
