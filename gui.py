import tkinter as tk   
from login import login_and_scan


class Application(tk.Frame):              
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)   
        self.grid(padx=50, pady=50)                       
        self.createWidgets()

    def createWidgets(self):

        def run_scan():

            center = self.center_name.get()
            login_id = self.user_id.get()
            password = self.password.get()
            scan_range = self.range.get()
            if center == '':
                print('working')
            login_and_scan(center, login_id, password, scan_range)


        self.label = tk.LabelFrame(self, text='Center Name')
        self.label.grid(pady=5)
        self.center_name = tk.Entry(self.label)
        self.center_name.grid()

        self.label = tk.LabelFrame(self, text='User ID')
        self.label.grid(pady=5)
        self.user_id = tk.Entry(self.label)
        self.user_id.grid()

        self.label = tk.LabelFrame(self, text='Password')
        self.label.grid(pady=5)
        self.password = tk.Entry(self.label, show='*')
        self.password.grid()

        self.label = tk.LabelFrame(self, text="Scan Range")
        self.label.grid(pady=5)
        self.range = tk.Scale(self.label, orient=tk.HORIZONTAL, from_=4, to=10)
        self.range.set(7)
        self.range.grid()

        self.scanButton = tk.Button(self, text='Start Scan',command=run_scan)            
        self.scanButton.grid(pady=(15, 0))            

app = Application()                       
app.master.title('Missed Swipe Report')    
app.mainloop()    