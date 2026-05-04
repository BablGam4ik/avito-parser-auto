# -*- coding: utf-8 -*-
import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

def clean_price(price_str):
    if price_str:
        cleaned = re.sub(r'[^\d]', '', price_str)
        return int(cleaned) if cleaned else 0
    return 0

print("🔄 Подключение к браузеру...")
driver = webdriver.Chrome(options=chrome_options)
print("✅ Подключено! Парсинг...")

url = "https://www.avito.ru/moskva/kvartiry?p=1&price_to=150000"
driver.get(url)

wait = WebDriverWait(driver, 15)
wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '[data-marker="item"]')))
time.sleep(3)

items = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
print(f"🔍 Найдено карточек: {len(items)}")

all_apartments = []

for idx, item in enumerate(items, 1):
    try:
        # Название
        try:
            title = item.find_element(By.CSS_SELECTOR, 'h3').text.strip()
        except:
            title = "Квартира"

        # Цена
        try:
            price_elem = item.find_element(By.CSS_SELECTOR, '[data-marker="item-price"]')
            price_raw = price_elem.text.strip()
        except:
            price_raw = "0"
        price = clean_price(price_raw)

        # Адрес
        try:
            address = item.find_element(By.CSS_SELECTOR, '[data-marker="item-address"]').text.strip()
        except:
            address = "Адрес не указан"

        # Ссылка
        try:
            link = item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
        except:
            link = ""

        # Фото
        img_url = ""
        try:
            img_elements = item.find_elements(By.TAG_NAME, 'img')
            for img in img_elements:
                src = img.get_attribute('src')
                if src and 'avito.st' in src and 'stores_entrypoint' not in src:
                    img_url = src
                    break
        except:
            pass

        # Сохраняем
        apartment = {
            'title': title,
            'price': price,
            'price_raw': price_raw,
            'address': address,
            'link': link,
            'img': img_url
        }
        all_apartments.append(apartment)

        print(f"  {idx}. {title[:40]} - {price:,} ₽".replace(',', ' '))
        if img_url:
            print(f"     📷 ЕСТЬ ФОТО!")

    except Exception as e:
        print(f"  ❌ Ошибка {idx}: {e}")

print(f"\n🎉 Собрано {len(all_apartments)} квартир!")

with open('avito_apartments.json', 'w', encoding='utf-8') as f:
    json.dump(all_apartments, f, ensure_ascii=False, indent=2)

print("💾 Сохранено в avito_apartments.json")