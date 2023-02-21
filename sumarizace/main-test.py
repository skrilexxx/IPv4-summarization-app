import dearpygui.dearpygui as dpg

sirka = 600
vyska = 600

dpg.create_context()
dpg.create_viewport(title='Sumarizace IPv4', width=sirka, height=vyska)

def vstup(sender,app_data,user_data):
		if dpg.get_value("binary"):
			input = int(dpg.get_value(sender))
			bin_out = bin(input)
			dpg.set_value("Vysledek", str(bin_out[2:]))
		else:
			dpg.set_value("Vysledek", dpg.get_value(sender))

#tady chci funkci co bude pridavat radky na ip (nefunguje jeste)
def add_radek():
	with dpg.group(horizontal=True):
		dpg.add_text("IP address:")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_1", decimal=(True)) #IP_1 (- první IP) _1 (- část IP 1-5, 5= prefix)
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_2", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_3", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_4", decimal=(True))
		dpg.add_text("/")
		dpg.add_input_text(default_value="**", on_enter=True, callback=vstup, width=20, tag="IP_1_5", decimal=(True))

		dpg.add_text(tag="Vysledek")

#získá celou Ip z inputu
def get_full_ip():
	output = ""
	if ((dpg.get_value("IP_1_1") != "***") and (dpg.get_value("IP_1_1") != "") and (dpg.get_value("IP_1_4") != "***") and (dpg.get_value("IP_1_4") != "")):
		for i in range(4):
			output += str(dpg.get_value("IP_1_" + str(i+1)))
			output += "."
		dpg.set_value("test", output[:-1])

with dpg.window(tag="Primary Window", label="Sumarizace IPv4", width=sirka, height=vyska):
	#jeden řádek = jedna IP
	with dpg.group(horizontal=True):
		dpg.add_text("IP address:")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_1", decimal=(True)) #IP_1 (- první IP) _1 (- část IP 1-5, 5= prefix)
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_2", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_3", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True, callback=vstup, width=30, tag="IP_1_4", decimal=(True))
		dpg.add_text("/")
		dpg.add_input_text(default_value="**", on_enter=True, callback=vstup, width=20, tag="IP_1_5", decimal=(True))

		dpg.add_text(tag="Vysledek")

	dpg.add_button(label="+", tag="plus_button", callback=add_radek) #přidá další řádek na IP
	dpg.add_button(label="Count", callback=get_full_ip) #spočítá sumarizační ip adresu
	dpg.add_checkbox(label="Binární", tag="binary") #pokud checked - vypíše je v binárním tvaru
	dpg.add_text(label="Test: ", tag="test") #testovaci output

dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()