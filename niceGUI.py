from nicegui import ui, run
import asyncio
from login import login_and_scan

async def run_scan():
    if center.value == None:
        ui.notify('You must select a center')
    else:
        try:
            ui.notify('Scanning, please wait.')
            await asyncio.sleep(1)
            await login_and_scan(center.value, login_id.value, password.value, scan_range.value)
        except:
            ui.notify('Somthing went wrong. Please try again')
        finally:
            await asyncio.sleep(1)
            
with ui.card().classes('items-center w-full no-shadow'):
    with ui.card():

        label = ui.label("Missed Swipe Report").classes('text-2xl font-bold')

        center = ui.select(['AOTK', 'Agape', 'All Day Daycare', 'Right Start'], new_value_mode=None, with_input=True,label='Choose a center').classes('required:border-red-500')

        login_id = ui.input(label='Login ID',
                on_change=lambda e: login_id.set_value(e.value))

        password = ui.input(label='Password',
                on_change=lambda e: password.set_value(e.value))
        
        label = ui.label("Scan Range")
        scan_range = ui.slider(min=4, max=10, value=7, on_change=lambda e: scan_range.set_value(e.value))
        with ui.row():
            label = ui.label().bind_text_from(scan_range, 'value')
            label = ui.label("Days ago")

        run_scan_btn = ui.button('RUN SCAN!', on_click=run_scan)

ui.run(native=False, favicon='🚀', title="Missed Swipe Report")

