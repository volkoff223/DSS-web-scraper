from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import io
from datetime import date
import datetime



today = datetime.datetime.now()
first_date_of_month = today.replace(day=1)


def login_and_scan(center, id, password):
    # Selenium to login and get to correct page
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get("https://www.vaecc.org/eccpw")
    el_username = driver.find_element(By.NAME, "login")
    el_username.send_keys(id)
    el_password = driver.find_element(By.NAME, "password")
    el_password.send_keys(password)
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

    # Grab table from html and remove all unusable data
    pd.options.mode.copy_on_write = True
    html = io.StringIO(driver.page_source)
    data = pd.read_html(html, match='provider_attendance')
    #grab correct table
    df = data[3]
    #remove usless data
    df.drop([0,1,2,3,4], inplace=True)
    #reset index
    df.reset_index(drop=True, inplace=True)
    #remove last nine lines
    df=df[:-9]
    #remove multi level column name
    df.columns = df.columns.droplevel()
    #remove usless columns
    df.drop(columns=df.columns[1:4], inplace=True)
    #remove dates in the future
    df.drop(columns=df.columns[9:], inplace=True) ## change 9 to todays date

    # rename all column names to date
    index = 1
    while index < len(df.columns):
        df.rename(columns={str(index): first_date_of_month.replace(day=index).strftime('%a %d')}, inplace=True)
        index +=1

    # # remove weekend
    for date in df.columns:
        if date.startswith('S'):
            df.drop([date], axis=1, inplace=True)

    inconplete_scan = []
    no_scan = []
    for idate in df.columns:
        for idx in df.index:
            if df.loc[idx][idate] == 'I':
                inconplete_scan_info = df.iloc[idx, 0] +" "+ idate + today.strftime('%B')
                inconplete_scan.append(inconplete_scan_info)

            elif type(df.loc[idx][idate]) == float:
                no_scan_info = df.iloc[idx, 0] +" "+ idate + today.strftime('%B')
                no_scan.append(no_scan_info)

    print('INCOMPLETE SCANS:', inconplete_scan, 'NO SCANS:', no_scan)
    file = open(center + '.txt', 'w')
    file.write(center)
    file.write("\nINCOMPLETE SCANS:\n")
    for scan in inconplete_scan:
        file.write(scan+'\n')
    file.write("\nNO SCAN:\n")
    for nscan in no_scan:
        file.write(nscan+'\n')
    file.close()
    # driver.close()