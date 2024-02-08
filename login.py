from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd

username = "511002120"
passwrd = "Bailey1028"

options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")
driver = webdriver.Chrome(options=options)
driver.get("https://www.vaecc.org/eccpw")
el_username = driver.find_element(By.NAME, "login")
el_username.send_keys(username)
el_password = driver.find_element(By.NAME, "password")
el_password.send_keys(passwrd)
el_login_btn = driver.find_element(By.CLASS_NAME, "login-btn")
el_login_btn.click()
cont_btn = driver.find_element(By.TAG_NAME, 'button')
cont_btn.click()
cont_btn = driver.find_element(By.NAME, 'contin')
cont_btn.click()
report_button = driver.find_element(By.XPATH, '//button[contains(text(),"ATTENDANCE REPORT")]')
report_button.click()
max_rows = driver.find_element(By.NAME, "maxRows")
max_rows.click()
option = driver.find_element(By.XPATH, '//option[contains(text(), "100")]')
option.click()

html = driver.page_source
df = pd.read_html(html, match='provider_attendance')
df[3].to_csv('text.csv')

driver.close()