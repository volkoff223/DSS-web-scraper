
import pandas as pd



data = {'Name':[], 'Date':[]}

data["Name"] += ['Nick']
data["Name"] += ['Bob']
data["Name"] += ['Jack']
data["Date"] += ['24567']
data["Date"] += ['58675']
data["Date"] += ['29786']



df = pd.DataFrame(data)
print(df)