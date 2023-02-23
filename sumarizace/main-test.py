import dearpygui.dearpygui as dpg

sirka = 600
vyska = 600
pocet = 1

dpg.create_context()
dpg.create_viewport(title='Sumarizace IPv4', width=sirka, height=vyska)

def vstup(sender,app_data,user_data):
		if dpg.get_value("binary"):
			input = int(dpg.get_value(sender))
			bin_out = bin(input)
			dpg.set_value("Vysledek_n", str(bin_out[2:]))
		else:
			dpg.set_value("Vysledek_n", dpg.get_value(sender))

#tady chci funkci co bude pridavat radky na ip (funguje na 50% jeste)
def add_radek(pocet):
	with dpg.group(horizontal=True):
		dpg.add_text("IP address:")
		dpg.add_input_text(default_value="***", on_enter=True,  width=30, tag="IP_"+ str(pocet) +"_1", decimal=(True)) #IP_1 (- první IP) _1 (- část IP 1-5, 5= prefix)
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True,  width=30, tag="IP_"+ str(pocet) +"_2", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True,  width=30, tag="IP_"+ str(pocet) +"_3", decimal=(True))
		dpg.add_text(".")
		dpg.add_input_text(default_value="***", on_enter=True,  width=30, tag="IP_"+ str(pocet) +"_4", decimal=(True))
		dpg.add_text("/")
		dpg.add_input_text(default_value="**", on_enter=True,  width=20, tag="IP_"+ str(pocet) +"_5", decimal=(True))

		dpg.add_text(tag="Vysledek_" + str(pocet))

	dpg.set_value("Vysledek_" + str(pocet), "")
	pocet += 1

#získá celou Ip z inputu, v D i B
def get_full_ip():
	for i in range(pocet):
		output = ""
		if ((dpg.get_value("IP_"+ str(i+1) +"_1") != "***") and (dpg.get_value("IP_"+ str(i+1) +"_1") != "") and (dpg.get_value("IP_"+ str(i+1) +"_4") != "***") and (dpg.get_value("IP_"+ str(i+1) +"_4") != "")):
			if dpg.get_value("binary"):
				for y in range(4):
					output += str(bin(int(dpg.get_value("IP_"+ str(i+1) +"_" + str(y+1))))[2:])
					output += "."
				dpg.set_value("Vysledek_" + str(i+1), output[:-1])			
			else:	
				for x in range(4):
					output += str(dpg.get_value("IP_"+ str(i+1) +"_" + str(x+1)))
					output += "."
				dpg.set_value("Vysledek_" + str(i+1), output[:-1])
		else:
			dpg.set_value("Vysledek_" + str(i+1), "Zkontrolujte zadanout")

with dpg.window(tag="Primary Window", label="Sumarizace IPv4", width=sirka, height=vyska):

	dpg.add_button(label="+", tag="plus_button", callback=add_radek(pocet)) #přidá další řádek na IP
	dpg.add_button(label="Count", callback=get_full_ip) #spočítá sumarizační ip adresu
	dpg.add_checkbox(label="Binární", tag="binary") #pokud checked - vypíše je v binárním tvaru
	dpg.add_text(label="Test: ", tag="test") #testovaci output

dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()