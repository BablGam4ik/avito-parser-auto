import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://www.avito.ru/moskva/kvartiry")

time.sleep(5)

# Прокручиваем
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(2)

# Находим все картинки
images = driver.find_elements(By.CSS_SELECTOR, 'img')
print(f"Всего img на странице: {len(images)}")

# Показываем первые 10
for i, img in enumerate(images[:10]):
    src = img.get_attribute('src')
    print(f"{i+1}. {src[:100] if src else 'Нет src'}")

driver.quit()