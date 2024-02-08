import pandas as pd
from datetime import date
import datetime
import numpy as np

file_to_read = 'table-data1.xls'
today = date.today()

#! this need to be user input
#input_month = int(input('What month is the file from (1 - 12):'))
#input_year = int(input('What year is the file from:'))
input_month = 1
input_year = 2024
file_date = datetime.date(input_year, input_month, 1)
df = pd.read_excel(file_to_read)

# remove unused colums
df.drop(df.iloc[:,1:4], inplace=True, axis=1)

# if reading file from this month remove dates in the future
if today.month == input_month:
    df.drop(df.iloc[:, today.day:], inplace=True, axis=1)


# rename all column names to date
index = 1
while index < len(df.columns):
    first_day = file_date
    df.rename(columns={str(index): first_day.replace(day=index).strftime('%a %d')}, inplace=True)
    index +=1

# remove weekend
for date in df.columns:
    if date.startswith('S'):
        df.drop([date], axis=1, inplace=True)

#! Scan only Wed to Wed
        


# search each column for 'I' and return Child Name and date
inconplete_scan = []
no_scan = []

for idate in df.columns:
    for idx in df.index:
        if df.loc[idx][idate] == 'I':
            inconplete_scan_info = df.iloc[idx, 0], idate, file_date.strftime('%B'), input_year
            inconplete_scan.append(inconplete_scan_info)

        elif type(df.loc[idx][idate]) == float:
            no_scan_info = df.iloc[idx, 0], idate, file_date.strftime('%B'), input_year
            no_scan.append(no_scan_info)

print(inconplete_scan_info)

#! Send email to center
