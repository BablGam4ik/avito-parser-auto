import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.avito.ru/moskva/kvartiry")

time.sleep(5)
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)

# Находим первую карточку
items = driver.find_elements(By.CSS_SELECTOR, '[data-marker="item"]')
if items:
    first_item = items[0]
    print("🔍 Анализируем первую карточку:")
    print(f"   Внутренний HTML: {first_item.get_attribute('innerHTML')[:500]}")

    # Ищем все img внутри карточки
    imgs = first_item.find_elements(By.CSS_SELECTOR, 'img')
    print(f"\n📷 Найдено img в карточке: {len(imgs)}")
    for i, img in enumerate(imgs):
        src = img.get_attribute('src')
        print(f"   {i + 1}. src: {src[:100] if src else 'None'}")

driver.quit()