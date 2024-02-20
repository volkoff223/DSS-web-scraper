from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import io
from datetime import date
import datetime
import shutil
import webbrowser




today = date.today()
first_date_of_month = today.replace(day=1)


def login_and_scan(center, id, password):
    # Selenium to login and get to correct page
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
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
    #remove usless columns and everything from 7 days ago
    df.drop(columns=df.columns[1:4], inplace=True)
    #remove dates in the future
    df.drop(columns=df.columns[today.day:], inplace=True)
    print(df)
 
    # rename all column names to date
    index = 1
    while index < len(df.columns):
        df.rename(columns={df.columns[index]: first_date_of_month.replace(day=index)}, inplace=True)
        index += 1
    #remove dates from begining of month to 7 days ago
    df.drop(columns=df.columns[1:today.day-7], inplace=True)
    
    # remove weekends
    for col in df.columns:
        if isinstance(col, datetime.date):
            if col.weekday() > 4:
                df.drop(columns=col, inplace=True)

    incomplete_scan = {"Name":[], "Date":[]}
    no_scan = {"Name":[], "Date":[]}
    for idate in df.columns:
        for idx in df.index:
            if df.loc[idx][idate] == 'I':
                incomplete_scan["Name"] += [df.iloc[idx, 0]]
                incomplete_scan["Date"] += [idate.strftime("%m/%d/%y")]

            if type(df.loc[idx][idate]) == float:
                no_scan["Name"] += [df.iloc[idx, 0]]
                no_scan["Date"] += [idate.strftime("%m/%d/%y")]
    
    df = pd.DataFrame(incomplete_scan)
    df1 = pd.DataFrame(no_scan)

    shutil.copyfile('style_template.html', 'DSS_report.html')

    f = open('scan_report.html', 'w')
    f.write('<h1>' + center + '</h1>' + '\n' + '<h3>Incomplete Scans</h3>' + '\n' + df.to_html(index=False) + '\n' + '<h3>No Scans</h3>' + '\n' + df1.to_html(index=False) + '\n' + '</body></html>')
    driver.close()
    driver.quit()
    webbrowser.open_new('scan_report.html')
    return
