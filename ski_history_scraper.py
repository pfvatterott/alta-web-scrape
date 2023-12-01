from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from datetime import datetime
import time

email = config("email")
password = config("password")

alta_url = "https://shop.alta.com/customer/login"

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

class SkiHistory:
    def __init__(self):
        self.driver = webdriver.Chrome(options=chrome_options)
        
    
    def login(self):
        self.driver.get(alta_url)
        self.driver.find_element(By.XPATH, value='//*[@id="checkout-login-email"]').send_keys(email)
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div/div/div/div/form/div[2]/button').click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, value='//*[@id="checkout-login-password"]').send_keys(password)
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div/div/div/div/form/div[2]/button').click()
        time.sleep(1)
        
    def enter_web_id(self, web_id):
        self.driver.find_element(By.XPATH, value='//*[@id="wtp-0"]').send_keys(web_id)
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div/form/div/div[2]/div/div/div/button').click()
        time.sleep(3)
        # TODO check if web ID is valid. If not, return error to frontend
        
    def get_ski_history(self):
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h4/a/i').click()
        time.sleep(3)
        return self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h5')
        
    def get_each_day(self):
        day_list = []
        each_day = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .row .col-12 div h6")
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
        return day_list
    
    def get_runs_each_day(self, day_list):
        runs_each_day = self.driver.find_elements(By.CSS_SELECTOR, ".card-body .row .col-12 div .table-responsive table")
        runs_in_day_index = 0
        for runs in runs_each_day:
            each_run = runs.text.split("\n")
            run_array = []
            for run in each_run:
                if "Lift Time" not in run:
                    obj = {
                        "lift": run.split(" ")[0],
                        "time": run.split(" ")[1] + " " + run.split(" ")[2] 
                    }
                    run_array.append(obj)
            day_list[runs_in_day_index]["runs"] = run_array
            runs_in_day_index += 1
            
        return day_list
        
        