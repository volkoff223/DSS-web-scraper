from tkinter import messagebox, ttk
from tkinter import filedialog as fd 
import tkinter as tk
import os

def display_selection():
    # Get the selected value.
    selection_year = input_year.get()
    selection_month = input_month.get()
    messagebox.showinfo(
        message=f"The selected year is: {selection_year}\nThe selected month is: {selection_month}",
        title="Selection"
    )
def open_file(): 
  
    # Specify the file types 
    filetypes = [('Excel file', '*.xls')] 
  
    # Show the open file dialog by specifying path 
    f = fd.askopenfile(filetypes=filetypes) 
  
    if f:
      filepath = os.path.abspath(f.name)
  

main_window = tk.Tk()
main_window.config(width=300, height=200)
main_window.title("Jen's Quick Scan")


# user input for month
label = ttk.Label(text="Please select a month:")
label.place(x=50, y=35)
input_month = ttk.Combobox(
    state="readonly",
    values=["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Nov", "Dec"]
)
input_month.place(x=50, y=50)


# user input for year
label = ttk.Label(text="Please select a year:")
label.place(x=50, y=85)
input_year = ttk.Combobox(
    state="readonly",
    values=["2024", "2025", "2026"]
)
input_year.place(x=50, y=100)

# Create an open file button 
label = ttk.Label(text="Please select a file:")
label.place(x=50, y=135)
open_button = ttk.Button(main_window, text='Open a File', command=open_file) 
open_button.place(x=50, y=150)

# Display selections
button = ttk.Button(text="Display selection", command=display_selection)
button.place(x=50, y=200)

# Create a textfield for putting the 
# text extracted from file 
text = tk.Text(main_window, height=12) 
  
# Specify the location of textfield 
text.grid(column=0, row=0, sticky='nsew') 
text.place(x=50, y=300)

main_window.mainloop()
