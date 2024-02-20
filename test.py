from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import date
import shutil
import webbrowser
import datetime

today = date.today()
first_date_of_month = today.replace(day=1)

df = pd.read_csv('test.csv')
   # rename all column names to date
index = 1
while index < len(df.columns):
    df.rename(columns={df.columns[index]: first_date_of_month.replace(day=index)}, inplace=True)
    index += 1

    #remove dates from begining of month to 7 days ago
#df.drop(columns=df.columns[1:today.day-8], inplace=True)
    
# remove weekends

for col in df.columns:
    if isinstance(col, datetime.date):
        if col.weekday() > 4:
            print(col)
            df.drop(columns=col, inplace=True)
print(df.columns)          


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
f.write('\n' + '<h3>Incomplete Scans</h3>' + '\n' + df.to_html(index=False) + '\n' + '<h3>No Scans</h3>' + '\n' + df1.to_html(index=False) + '\n' + '</body></html>')
webbrowser.open_new('scan_report.html')
