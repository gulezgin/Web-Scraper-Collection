import json
import requests 
from bs4 import BeautifulSoup
from csv import writer  
import pandas as pd
from tabulate import tabulate


"""
COUNTRY SCRAPING EXAMPLE

url = 'https://www.scrapethissite.com/pages/simple/'

response = requests.get(url)



soup = BeautifulSoup(response.text, 'html.parser')

countries = []

for country_div in soup.find_all("div", class_="col-md-4 country"):
    name = country_div.find("h3", class_="country-name").get_text(strip=True)
    capital = country_div.find("span", class_="country-capital").get_text(strip=True)
    population = country_div.find("span", class_="country-population").get_text(strip=True)
    area = country_div.find("span", class_="country-area").get_text(strip=True)
    
    countries.append({
        "name": name,
        "capital": capital,
        "population": population,
        "area_km2": area
    })

with open("countries.json", "w", encoding="utf-8") as f:
    json.dump(countries, f, ensure_ascii=False, indent=4)
"""



"""
CORONAVIRUS SCRAPING EXAMPLE

url = 'https://www.worldometers.info/coronavirus/'

response = requests.get(url)
response.raise_for_status()  # hata kontrolü

# HTML parse et
soup = BeautifulSoup(response.text, "html.parser")

# Ana tabloyu bul
table = soup.find("table", id="main_table_countries_today")

# Tablo başlıklarını al
headers = [header.text.strip() for header in table.find_all("th")]

# Tablo satırlarını al
rows = []
for row in table.find_all("tr")[1:]:
    cols = [col.text.strip() for col in row.find_all("td")]
    if cols:
        rows.append(cols)

df = pd.DataFrame(rows, columns=headers)

df.to_json("coronavirus_data.json", orient="records", force_ascii=False, indent=4)
"""
