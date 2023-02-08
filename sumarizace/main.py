import dearpygui.dearpygui as dpg

sirka = 600
vyska = 600

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=sirka, height=vyska)


with dpg.window(label="Sumarizace IPv4", width=sirka, height=vyska):
	dpg.add_text("IP address:")
	dpg.add_button(label="Count")
	dpg.add_input_text(label="string", default_value="Quick brown fox")
	dpg.add_slider_float(label="float", default_value=0.273, max_value=1)



dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()