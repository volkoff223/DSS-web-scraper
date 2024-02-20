import customtkinter
from datetime import date
from tkcalendar import Calendar
import time

from login import login_and_scan




class DSSReportFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master)

        
        def button_callback():
            id = self.center_login_id.get()
            password = self.center_password.get()
            center = self.center_combobox.get()

            
            
            self.label1.forget()
            self.center_combobox.forget()
            self.label2.forget()
            self.center_login_id.forget()
            self.label3.forget()
            self.center_password.forget()
            self.label4.forget()
            self.cal.forget()
            self.run_scan_button.forget()
            login_and_scan(center, id, password)

            

        self.label1 = customtkinter.CTkLabel(self, text="Choose a center", fg_color="transparent", width=300)
        self.label1.pack(padx=5, pady=5)

        center_combobox_var = customtkinter.StringVar(value="")
        self.center_combobox = customtkinter.CTkComboBox(self, values=['AOTK', 'Agapy', 'All Day Daycare', 'Right Start'], variable=center_combobox_var, width=300)
        self.center_combobox.set('')
        self.center_combobox.pack(padx=5, pady=5)
        center_combobox_var.set('')

        self.label2 = customtkinter.CTkLabel(self, text="Login ID", fg_color="transparent", width=300)
        self.label2.pack(padx=5, pady=5)

        self.center_login_id = customtkinter.CTkEntry(self, width=300)
        #! Remove
        self.center_login_id.insert(0, '511000186')
        self.center_login_id.pack(padx=5, pady=5)

        self.label3 = customtkinter.CTkLabel(self, text="Password", fg_color="transparent", width=300)
        self.label3.pack(padx=5, pady=5)

        self.center_password = customtkinter.CTkEntry(self, width=300)
        #! Remove 
        self.center_password.insert(0, '2023Blessings3!')
        self.center_password.pack(padx=5, pady=5)

        self.label4 = customtkinter.CTkLabel(self, text="Choose scan start date", fg_color="transparent", width=300)
        self.label4.pack(padx=5, pady=5)  

        self.cal = Calendar(self, selectmode = 'day', year = 2024, month = 2)
        self.cal.pack(padx=5, pady=5)




        self.run_scan_button = customtkinter.CTkButton(self, text="Create DSS Report", command=button_callback,  width=300)
        self.run_scan_button.pack(padx=5, pady=5)

        self.save_report_button = customtkinter.CTkButton(self, text="Save DSS Report", width=300)
        self.save_report_button.forget()


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DSS Scan Tool")
        self.geometry("600x600")


        self.dss_report_frame = DSSReportFrame(self)
        self.dss_report_frame.pack(expand=True, fill='both')





app = App()
app.mainloop()