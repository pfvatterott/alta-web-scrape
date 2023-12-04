from selenium import webdriver
from selenium.webdriver.common.by import By
from decouple import config
from datetime import datetime
import requests
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
        cookies_list = self.driver.get_cookies()
        cookieString = ""
        for cookie in cookies_list[:-1]:
            cookieString = cookieString + cookie["name"] + "="+cookie["value"]+"; "

        cookieString = cookieString  + cookies_list[-1]["name"] + "="+ cookies_list[-1]["value"]
        xsrf_token = cookieString.split("XSRF-TOKEN=")[1].split("; ")[0].replace("%3D", "=")
        return {
            "cookieString": cookieString,
            "xsrf_token": xsrf_token
        }
        
    def getSeasonId(self, web_id, cookies, xsrf_token): 
        req_params = {
            "wtp": web_id,
            "productId": 0
        }
        req_headers = {
            "Cookie": cookies,
            "X-Requested-With": "XMLHttpRequest",
            "X-Xsrf-Token": xsrf_token
        }

        response = requests.post(url="https://shop.alta.com/axess/ride-data", json=req_params, headers=req_headers)
        return response.json()
        
    def getSkiHistory(self, nposno, nprojno, nserialno, szvalidfrom, cookies, xsrf_token):
        req_params = {
            "nposno": nposno,
            "nprojno": nprojno,
            "nserialno": nserialno,
            "szvalidfrom": szvalidfrom
        }
        req_headers = {
            "Cookie": cookies,
            "X-Requested-With": "XMLHttpRequest",
            "X-Xsrf-Token": xsrf_token
        }

        response = requests.post(url="https://shop.alta.com/axess/rides", json=req_params, headers=req_headers)
        return response.json()  
    
        
        
    def enter_web_id(self, web_id):
        self.driver.find_element(By.XPATH, value='//*[@id="wtp-0"]').send_keys(web_id)
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div/form/div/div[2]/div/div/div/button').click()
        time.sleep(3)
        error_or_success_msg = self.driver.find_element(By.CLASS_NAME, value="feedback")
        if len(error_or_success_msg.text) > 0:
            self.driver.quit()
            return False
        
    def get_ski_history(self):
        self.driver.find_element(By.XPATH, value='//*[@id="app"]/main/section/div[3]/div/div/div[1]/div/div/div[3]/div/h4/a/i').click()
        time.sleep(5)
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
        
        