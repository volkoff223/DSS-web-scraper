from nicegui import ui
from login import login_and_scan

def run_scan():
    #await asyncio.sleep(10)
    login_and_scan(center.value, login_id.value, password.value)
    ui.notify('finished')


with ui.card():

    label = ui.label("Jen's DSS Scan Tool")

    center = ui.select(['AOTK', 'Agapy', 'All Day Daycare', 'Right Start'], new_value_mode=None, with_input=True,label='Choose a center')

    login_id = ui.input(label='Login ID', value='511000186',
            on_change=lambda e: login_id.set_value(e.value))


    password = ui.input(label='Password', value='2023Blessings3!',
            on_change=lambda e: password.set_value(e.value))

    start_date = ui.date(value='2023-01-01', on_change=lambda e: start_date.set_value(e.value))

    run_scan_btn = ui.button('RUN SCAN!', on_click=run_scan)


ui.run(favicon='🚀', title="Jen's DSS Scan Tool")

