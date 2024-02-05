import pandas as pd
from datetime import date

today = date.today()
month_number = int(input('What month number is the spreadsheet?: '))
year = int(input('What year is the spreadsheet?: '))

first_day_of_month = pd.to_datetime(year, month_number, 1)
print(first_day_of_month)


df = pd.read_excel('table-data.xls')

# return only names and dates from the 1st to todays date
# return all dates if reading a privious months data
if today.month == month_number:
    df.drop(df.iloc[:, today.day+4:], inplace=True, axis=1)

# remove unneed columns
df.drop(df.iloc[:,1:4], inplace=True, axis=1)

#this is not working
df.rename(columns={'1': first_day_of_month}, inplace=True)
print(df)
# Remove weekends



