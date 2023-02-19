import dearpygui.dearpygui as dpg

sirka = 600
vyska = 600

dpg.create_context()
dpg.create_viewport(title='Sumarizace IPv4', width=sirka, height=vyska)

def vstup(sender,app_data,user_data):
	dpg.set_value("Vysledek", dpg.get_value(sender))

with dpg.window(tag="Primary Window", label="Sumarizace IPv4", width=sirka, height=vyska):
	with dpg.group(horizontal=True):
		dpg.add_text("IP address:")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_first_segment")
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_second_segment")
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_third_segment")
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_fourht_segment")

	dpg.add_button(label="Count")
	dpg.add_text(tag="Vysledek")


dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()