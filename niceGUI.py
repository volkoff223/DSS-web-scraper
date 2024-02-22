

from nicegui import ui
from secure import passwrd, user_id
import time
import asyncio

from login import login_and_scan

async def run_scan():
    if center.value == None:
        ui.notify('You must select a center')
    else:
        ui.spinner(size='lg')
        run_scan_btn.disable()
        await asyncio.sleep(1)
        await login_and_scan(center.value, login_id.value, password.value)

        run_scan_btn.enable()



with ui.card().classes('items-center w-full no-shadow'):
    with ui.card():

        label = ui.label("Jen's DSS Scan Tool").classes('text-2xl font-bold')

        center = ui.select(['AOTK', 'Agape', 'All Day Daycare', 'Right Start'], new_value_mode=None, with_input=True,label='Choose a center').classes('required:border-red-500')

        login_id = ui.input(label='Login ID', value=user_id,
                on_change=lambda e: login_id.set_value(e.value))


        password = ui.input(label='Password', value=passwrd,
                on_change=lambda e: password.set_value(e.value))


        run_scan_btn = ui.button('RUN SCAN!', on_click=run_scan)


ui.run(native=True, favicon='🚀', title="Jen's DSS Scan Tool")

