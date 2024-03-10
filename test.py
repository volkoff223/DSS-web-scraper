
import pandas as pd
from datetime import timedelta, date
import datetime
import webbrowser



styles = '<head><style>table,td,th {border: solid thin;border-collapse: collapse;}td,th {padding: 7px;}</style></head>'

#! fake day must change back to "today=date.today()"
today = date.today().replace(day=9)



first_date_of_month = today.replace(day=1)
month, year = (first_date_of_month.month-1, first_date_of_month.year) if first_date_of_month != 1 else (12, first_date_of_month.year-1)
first_date_of_last_month = first_date_of_month.replace(month=month, year=year)
scan_days_range = 7
last_date_of_last_month = first_date_of_month - timedelta(days=1)

def login_and_scan(center):

    df = pd.read_csv('test_df.csv')  
    lmdf = pd.read_csv('LM_test_df.csv')
    #!-- This is where the logic is to pull df from website --#


    if today.day < 8:
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
                if today-timedelta(scan_days_range) <= col:
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

 
    # rename all column names to date
    index = 1
    while index < len(df.columns):
        df.rename(columns={df.columns[index]: first_date_of_month.replace(day=index)}, inplace=True)
        index += 1


    #remove dates from begining of month to scan range days
    if today.day > scan_days_range:
        df.drop(columns=df.columns[1:today.day-scan_days_range], inplace=True)


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


login_and_scan('AOTK')