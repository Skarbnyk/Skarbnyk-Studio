import dearpygui.dearpygui as dpg

import sys
sys.path.append('accounts')
from accounts import *

if __name__ == '__main__':
    dpg.create_context()
    #dpg.configure_app(manual_callback_management=True)
    dpg.create_viewport(title='Skarbnyk Studio', width=1920, height=1080)
    dpg.setup_dearpygui()

    with dpg.window(label='Skarbnyk Studio', tag='MainWindow', no_title_bar=True):
        dpg.add_text('Skarbnyk Studio')

        with dpg.tab_bar():
            with dpg.tab(label='Accounts'):

                with dpg.table(header_row=True, borders_innerH=True, borders_outerH=True, borders_innerV=True,
                               borders_outerV=True, resizable=True, row_background=True, no_host_extendX=True,
                               policy=dpg.mvTable_SizingFixedFit):
                    dpg.add_table_column(label='Name')
                    dpg.add_table_column(label='EVM address')

                    for i in range(len(Accounts)):
                        account = Accounts[i]
                        with dpg.table_row():
                            dpg.add_text(account.name)
                            dpg.add_text(account.address)


    dpg.show_viewport()
    dpg.set_primary_window('MainWindow', True)
    dpg.start_dearpygui() #comment for debugging

    #while dpg.is_dearpygui_running():
    #    jobs = dpg.get_callback_queue()  # retrieves and clears queue
    #    dpg.run_callbacks(jobs)
    #    dpg.render_dearpygui_frame()

    dpg.destroy_context()

