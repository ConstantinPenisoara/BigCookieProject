from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime as dt

# Clicking the cookie for 56 seconds
TIMEOUT = 5

# Total gameplay time - 5 minutes
TOTAL_TIME = 300

# Time at the start of the game
timeout_start = time.time()

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get('https://orteil.dashnet.org/experiments/cookie/')

# Identifies the cookie
cookie = driver.find_element(By.ID, value="cookie")

# Starting the game which will last for 5 minyes
while time.time() < timeout_start + TOTAL_TIME:
    # Starting the clisk-the-cookie cycle of 5 seconds
    timeout_start_cycle = time.time()
    while time.time() < timeout_start_cycle + TIMEOUT:
        cookie.click()
    # delaying the app for half a second so that the number of cookies is properly registered by the app
    time.sleep(0.5)

    # Checking the available money/cookies
    available_money = int(driver.find_element(By.ID, value="money").text.replace(",", ""))

    # Initializing the list which will store the option/purchasable add-on: value dictionary
    options = []

    # Getting hod of the prices of the purchasable add-ons
    items = driver.find_elements(By.CSS_SELECTOR, value="#store")
    for item in items:
        prices = item.find_elements(By.TAG_NAME, value="b")
        for price in prices:
            try:
                price.text.split("-")[1].replace(",","")
            except IndexError:
                continue
            else:
                # If we can afford the add-ons, the option/purchasable add-on along with its price/value will be added
                # to the "options" list in the form of a dictionary
                if available_money > int(price.text.split("-")[1].replace(",","")):
                    options.append({price: int(price.text.split("-")[1].replace(",", ""))})

    # Clicking the most expensive available option/purchasable add-on, which is registered as the last dictionary in
    # the "options" list
    for key in options[-1].keys():
        key.click()
    # The "options" list is cleared for the next 5 seconds cycle of clicking the cookie
    options.clear()

# Getting the number of cookies per second that the player scored
cookies_per_second = driver.find_element(By.ID, value="cps").text.split(":")[1]

# Exiting the game
driver.quit()

# Getting the current date
now_date = str(dt.datetime.now()).split()[0].strip()

# Getting the current time
now_time = str(dt.datetime.now()).split()[1].split(".")[0].strip()

# Writing the number of cookies per second to file
with open("score.txt", "a") as file:
    file.write(f"On {now_date}, {now_time} you averaged {cookies_per_second.strip()} cookies per second.\n")



