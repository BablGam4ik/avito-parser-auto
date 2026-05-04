import time
import json
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def clean_price(price_str):
    if price_str:
        cleaned = re.sub(r'[^\d]', '', price_str)
        return int(cleaned) if cleaned else 0
    return 0


def parse_avito():
    """Парсинг Авито в headless-режиме (для GitHub Actions)"""

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("✅ Браузер запущен в headless-режиме")
    except Exception as e:
        print(f"❌ Ошибка запуска браузера: {e}")
        return []

    url = "https://www.avito.ru/moskva/kvartiry?p=1&price_to=150000"
    driver.get(url)
    time.sleep(5)

    items = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
    print(f"🔍 Найдено карточек: {len(items)}")

    all_apartments = []

    for idx, item in enumerate(items[:50], 1):
        try:
            # Название
            try:
                title_elem = item.find_element(By.CSS_SELECTOR, '[data-marker*="title"]')
                title = title_elem.text.strip()
            except:
                title_elem = item.find_element(By.CSS_SELECTOR, 'h3')
                title = title_elem.text.strip()

            # Цена
            try:
                price_elem = item.find_element(By.CSS_SELECTOR, '[data-marker*="price"]')
                price_raw = price_elem.text.strip()
            except:
                price_elem = item.find_element(By.CSS_SELECTOR, 'span[itemprop="price"]')
                price_raw = price_elem.get_attribute("content") or price_elem.text.strip()

            # Адрес
            try:
                address_elem = item.find_element(By.CSS_SELECTOR, '[data-marker*="address"]')
                address = address_elem.text.strip()
            except:
                address = "Адрес не указан"

            # Ссылка
            try:
                link_elem = item.find_element(By.CSS_SELECTOR, 'a')
                link = link_elem.get_attribute('href')
            except:
                link = ""

            # Фото
            img_url = ""
            try:
                img_elem = item.find_element(By.CSS_SELECTOR, 'img')
                img_url = img_elem.get_attribute('src')
                if img_url and '/50x50/' in img_url:
                    img_url = img_url.replace('/50x50/', '/600x600/')
            except:
                pass

            price = clean_price(price_raw)

            if price < 1000 and len(title) < 5:
                continue

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

        except Exception as e:
            print(f"  ❌ Ошибка в карточке {idx}: {e}")
            continue

    driver.quit()
    return all_apartments


if __name__ == "__main__":
    print("🚀 Запуск парсинга Авито...")
    apartments = parse_avito()

    with open('avito_apartments.json', 'w', encoding='utf-8') as f:
        json.dump(apartments, f, ensure_ascii=False, indent=2)

    print(f"✅ Сохранено {len(apartments)} квартир в avito_apartments.json")