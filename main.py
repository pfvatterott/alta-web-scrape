from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from datetime import datetime
import time

web_id = config("web_id")
email = config("email")
password = config("password")

alta_url = "https://shop.alta.com/customer/login"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get(alta_url)


# Logging in
driver.find_element(By.XPATH, value='//*[@id="checkout-login-email"]').send_keys(email)
driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div/div/div/div/form/div[2]/button').click()
time.sleep(1)
driver.find_element(By.XPATH, value='//*[@id="checkout-login-password"]').send_keys(password)
driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div/div/div/div/form/div[2]/button').click()

time.sleep(1)

# Enter Web ID
driver.find_element(By.XPATH, value='//*[@id="wtp-0"]').send_keys(web_id)
driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div/form/div/div[2]/div/div/div/button').click()

time.sleep(3)

# Get Ski History
driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h4/a/i').click()
time.sleep(3)
total_ft_and_days = driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h5')

# Yearly Totals
total_days = total_ft_and_days.text.split("SKIED: ")[1]
total_ft = total_ft_and_days.text.split("TOTAL VERTICAL FEET ")[1].split(", NUMBER")[0]

# Individual days
day_list = []
each_day = driver.find_elements(By.CSS_SELECTOR, ".card-body .row .col-12 div h6")
for day in each_day:
    feet = int(day.text.split("\n")[0].split("VERTICAL FEET ")[1].replace(",", ""))
    date = day.text.split("\n")[1].split(", ")[1]
    date = date.lower().replace("rd", "").replace("nd", "").replace("st", "").replace("th", "")
    date = datetime.strptime(date, "%B %d %Y").strftime("%m/%d/%Y")
    obj = {
        "date": date,
        "feet": feet
    }
    day_list.append(obj)

average_ft_per_day = int(total_ft.replace(",", "")) / int(total_days)
print(average_ft_per_day)