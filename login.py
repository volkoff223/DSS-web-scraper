from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import pandas as pd
import io
from datetime import timedelta, date
import datetime
import webbrowser
import shutil



styles = '<head><style>table,td,th {border: solid thin;border-collapse: collapse;}td,th {padding: 7px;}</style></head>'

today = date.today()



first_date_of_month = today.replace(day=1)
month, year = (first_date_of_month.month-1, first_date_of_month.year) if first_date_of_month != 1 else (12, first_date_of_month.year-1)
first_date_of_last_month = first_date_of_month.replace(month=month, year=year)
last_date_of_last_month = first_date_of_month - timedelta(days=1)




def login_and_scan(center, id, password, scan_range):

    # Selenium to login and get to correct page
    service = Service()
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)
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

    # Grab last month if current date is in first week of month

    if today.day<8:
        driver.find_element(By.NAME, "monthYear").click()
        driver.find_element(By.XPATH, '//*[@id="monthYear"]/option[2]').click()
        driver.find_element(By.XPATH, '//*[@id="content_table"]/tbody/tr/td/table/tbody/tr[4]/td/button').click()
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
        lmdf.drop([0,1,2,3,4], inplace=True)
        #reset index
        lmdf.reset_index(drop=True, inplace=True)
        #remove last nine lines
        lmdf=lmdf[:-9]
        #remove multi level column name
        #lmdf.columns = df.columns.droplevel()
        #remove usless columns and everything from
        lmdf.drop(columns=lmdf.columns[1:4], inplace=True)

        # remove columns from end of df that are not dates (ie 30 and 31 from feb)
        lmdf.drop(columns=lmdf.columns[int(last_date_of_last_month.day) + 1:], inplace=True)
 
        # rename all column names to date
        index = 1
        while index < len(lmdf.columns):
            lmdf.rename(columns={lmdf.columns[index]: first_date_of_last_month.replace(day=index)}, inplace=True)
            index += 1


        #remove dates from begining of last month to 7 days ago
        nlmdf = pd.DataFrame(lmdf[['Child Name']])
        for col in lmdf.columns:
            if isinstance(col, datetime.date):
                if today-timedelta(scan_range) <= col:
                    nlmdf.loc[:, col] = lmdf.loc[:, col]
        lmdf = nlmdf

        # remove weekends
        for col in lmdf.columns:
            if isinstance(col, datetime.date):
                if col.weekday() > 4:
                    lmdf.drop(columns=col, inplace=True)
        
        last_month_incomplete_scan = {"Name":[], "Date":[]}
        last_month_no_scan = {"Name":[], "Date":[]}
        for idate in lmdf.columns:
            for idx in lmdf.index:
                if lmdf.loc[idx][idate] == 'I':
                    last_month_incomplete_scan["Name"] += [lmdf.iloc[idx, 0]]
                    last_month_incomplete_scan["Date"] += [idate.strftime("%m/%d/%y")]

                if type(lmdf.loc[idx][idate]) == float:
                    last_month_no_scan["Name"] += [lmdf.iloc[idx, 0]]
                    last_month_no_scan["Date"] += [idate.strftime("%m/%d/%y")]
        lmisdf = pd.DataFrame(last_month_incomplete_scan)
        lmnsdf = pd.DataFrame(last_month_no_scan)
    

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
    #remove last nine rows
    df=df[:-9]

    #remove usless columns and everything from
    df.drop(columns=df.columns[1:4], inplace=True)

    #remove dates in the future
    df.drop(columns=df.columns[today.day:], inplace=True)

    #remove multi-level columns
    df.columns = df.columns.droplevel(0)
    
    # rename all column names to date
    index = 1
    while index < len(df.columns):
        df.rename(columns={df.columns[index]: first_date_of_month.replace(day=index)}, inplace=True)
        index += 1


    #remove dates from begining of month to scan range days
    if today.day > scan_range:
        df.drop(columns=df.columns[1:today.day-scan_range], inplace=True)


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
    
    isdf = pd.DataFrame(incomplete_scan)
    nsdf = pd.DataFrame(no_scan)
    if today.day<8:
        isdf = pd.concat([lmisdf, isdf])
        nsdf = pd.concat([lmnsdf, nsdf])


    html = f"{styles}\n<h1>{center}</h1>\n<h3>Incomplete Scans</h3>\n{isdf.to_html(index=False, header=False, border='0')}\n<h3>No Scans</h3>\n{nsdf.to_html(index=False, header=False, border='0')}\n</></html>"

    f = open(f'{center}_scan_report.html', 'w')
    f.write(html)
    webbrowser.open_new(f'{center}_scan_report.html')
