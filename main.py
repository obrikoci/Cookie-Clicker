from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_opt = webdriver.ChromeOptions()
chrome_opt.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_opt)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, "cookie")

upgrade_items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in upgrade_items]

timeout = time.time() + 5
finish_time = time.time() + 60*5

while True:
    cookie.click()

    if time.time() > timeout:
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        prices = []

        for price in all_prices:
            cost_text = price.text
            if cost_text != "":
                cost = int(cost_text.split("-")[1].strip().replace(",",""))
                prices.append(cost)

        upgraded_prices = {}
        for n in range(len(prices)):
            upgraded_prices[prices[n]] = item_ids[n]

        cookie_money = driver.find_element(By.ID, "money").text
        if "," in cookie_money:
            cookie_money = cookie_money.replace(",","")
        money = int(cookie_money)

        affordable_upgrades = {}
        for cost, id in upgraded_prices.items():
            if money > cost:
                affordable_upgrades[cost] = id

        highest_upgrade = max(affordable_upgrades)
        purchase_id = affordable_upgrades[highest_upgrade]
        driver.find_element(By.ID, purchase_id).click()

        timeout = time.time() + 5

    if time.time() > finish_time:
        cookies_per_sec = driver.find_element(By.ID, "cps").text
        print(f"Cookies/sec after 5 minutes: {cookies_per_sec}")
        break
