from nicegui import ui
from login import login_and_scan
from secure import passwrd, user_id

def run_scan():
    login_and_scan(center.value, login_id.value, password.value)



with ui.card():

    label = ui.label("Jen's DSS Scan Tool")

    center = ui.select(['AOTK', 'Agapy', 'All Day Daycare', 'Right Start'], new_value_mode=None, with_input=True,label='Choose a center')

    login_id = ui.input(label='Login ID', value=user_id,
            on_change=lambda e: login_id.set_value(e.value))


    password = ui.input(label='Password', value=passwrd,
            on_change=lambda e: password.set_value(e.value))


    run_scan_btn = ui.button('RUN SCAN!', on_click=run_scan)


ui.run(favicon='🚀', title="Jen's DSS Scan Tool")

