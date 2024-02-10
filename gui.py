import customtkinter

from login import login_and_scan


class DSSReportFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        
        def button_callback():
            id = self.center_login_id.get()
            password = self.center_password.get()
            center = self.center_combobox.get()
            login_and_scan(center, id, password)
            print(center, id, password)
            

        self.label = customtkinter.CTkLabel(self, text="Choose a center", fg_color="transparent", width=300)
        self.label.grid(row=0, column=0, pady=0)

        center_combobox_var = customtkinter.StringVar(value="")
        self.center_combobox = customtkinter.CTkComboBox(self, values=['AOTK', 'Agapy', 'All Day Daycare', 'Right Start'], variable=center_combobox_var, width=300)
        self.center_combobox.set('')
        self.center_combobox.grid(row=1, column=0, padx=10, pady=0)
        center_combobox_var.set('')

        self.label = customtkinter.CTkLabel(self, text="Login ID", fg_color="transparent", width=300)
        self.label.grid(row=2, column=0, pady=(10,0))

        self.center_login_id = customtkinter.CTkEntry(self, width=300)
        self.center_login_id.grid(row=3, column=0, padx=10, pady=0)

        self.label = customtkinter.CTkLabel(self, text="Password", fg_color="transparent", width=300)
        self.label.grid(row=4, column=0, pady=(10,0))

        self.center_password = customtkinter.CTkEntry(self, width=300)
        self.center_password.grid(row=5, column=0, padx=10, pady=0)


        self.button = customtkinter.CTkButton(self, text="Create DSS Report", command=button_callback, width=300)
        self.button.grid(row=6, column=0, padx=10, pady=10)



class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("DSS Scan Tool")
        self.geometry("600x400")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.dss_report_frame = DSSReportFrame(self)
        self.dss_report_frame.grid(row=0, column=0, padx=10, pady=10)



app = App()
app.mainloop()