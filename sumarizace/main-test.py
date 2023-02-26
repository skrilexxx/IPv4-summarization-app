import dearpygui.dearpygui as dpg

#ve finalnim programu to bude classa

sirka = 600
vyska = 600
pocet = 1
list_of_IPs = []
prefixList = []

dpg.create_context()
dpg.create_viewport(title='Sumarizace IPv4', width=sirka, height=vyska)

def vstup(sender,app_data,user_data):
		if dpg.get_value("binary"):
			input = int(dpg.get_value(sender))
			bin_out = bin(input)
			dpg.set_value("Vysledek_n", str(bin_out[2:]))
		else:
			dpg.set_value("Vysledek_n", dpg.get_value(sender))

def limit(sender, app_data, user_data):
	"""Limituje vstup 0-255"""
	if app_data != "":
		if int(app_data) < 0:
			dpg.set_value(sender, "0")
		elif int(app_data) > 255:
			dpg.set_value(sender, "255")
	elif len(app_data) > user_data:
		dpg.set_value(sender, app_data[:user_data])

def add_radek():
	"""Pridani radku na IP"""
	global pocet
	with dpg.group(tag="radek_" + str(pocet), horizontal=True, parent="radky"):
		dpg.add_text("IP address:")
		dpg.add_input_text(hint="***", width=30, tag=f"IP_{pocet}_1", decimal=True, callback=limit, user_data=3) #IP_1 (- první IP) _1 (- část IP 1-5, 5= prefix)
		dpg.add_text(".")
		dpg.add_input_text(hint="***", width=30, tag=f"IP_{pocet}_2", decimal=True, callback=limit, user_data=3)
		dpg.add_text(".")
		dpg.add_input_text(hint="***", width=30, tag=f"IP_{pocet}_3", decimal=True, callback=limit, user_data=3)
		dpg.add_text(".")
		dpg.add_input_text(hint="***", width=30, tag=f"IP_{pocet}_4", decimal=True, callback=limit, user_data=3)
		dpg.add_text("/")
		dpg.add_input_text(hint="**", width=20, tag=f"IP_{pocet}_5", decimal=True, callback=limit, user_data=2)

		dpg.add_text(tag="Vysledek_" + str(pocet))

	dpg.set_value("Vysledek_" + str(pocet), "")
	pocet += 1

def remove_radek():
	"""Smaže poslední řádek"""
	global pocet
	if pocet > 3:
		pocet -= 1
		dpg.delete_item("radek_" + str(pocet))

def min_max(listIp, prefixList) -> list[str]:
	"""Najde nejvetsi[0] a nejmesi[1] IP addresu (a nejmensi prefix) """
	return [max(listIp), min(listIp), min(prefixList)]

def sumarization():
	"""Spočíta sumarizační IP adresu"""
	global list_of_IPs
	global prefixList
	BigSmallIp = min_max(list_of_IPs, prefixList)
	print(BigSmallIp)

	max = BigSmallIp[0].split(".")
	min = BigSmallIp[1].split(".")
	prefix = BigSmallIp[2]
	sumZeros = 0
	maxPrefix = 32
	finalPrefix = 0

	maxBin = []
	minBin = []
	sumBin = []
	sumIp = ""
	same = True

	for i in range(len(max)):
		maxBin.append(bin(int(max[i]))[2:].zfill(8))
		minBin.append(bin(int(min[i]))[2:].zfill(8))

	print(maxBin, minBin)

	for i in range(len(maxBin)):

		sumSeg = ""
		for y in range(len(maxBin[i])):
			if same and maxBin[i][y] == minBin[i][y]:
				sumSeg = sumSeg + str(maxBin[i][y])
			else:
				same = False
			if same == False:
				sumSeg = sumSeg + "0"
				sumZeros += 1
		print(sumSeg)
		sumBin.append(sumSeg)
	print(sumBin)

	if (maxPrefix-sumZeros) == prefix:
		finalPrefix = prefix
	elif (maxPrefix-sumZeros) > prefix:
		finalPrefix = prefix
	else:
		finalPrefix = (maxPrefix-sumZeros)

	for number in sumBin:
		sumIp += str(int(number, 2))+"."

	dpg.set_value("VysledekSumarizace", sumIp[:-1] + " / " + str(finalPrefix))

def get_full_ip():
	"""získá celou Ip z inputu, v D i B"""
	global list_of_IPs
	global prefixList
	prefixList.clear()
	list_of_IPs.clear()
	IpList = []
	for i in range(pocet-1):
		output = ""
		outputBin = ""
		if ((dpg.get_value("IP_"+ str(i+1) +"_1") != "") and  (dpg.get_value("IP_"+ str(i+1) +"_4") != "") and (dpg.get_value("IP_"+ str(i+1) +"_5") != "")):
			if dpg.get_value("binary"):
				for y in range(4):
					outputBin += str(bin(int(dpg.get_value("IP_"+ str(i+1) +"_" + str(y+1))))[2:]).zfill(8)
					outputBin += "."
					output += str(dpg.get_value("IP_"+ str(i+1) +"_" + str(y+1)))
					output += "."
				IpList.append(output[:-1])
				prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
				dpg.set_value("Vysledek_" + str(i+1), outputBin[:-1])
			else:
				for x in range(4):
					output += str(dpg.get_value("IP_"+ str(i+1) +"_" + str(x+1)))
					output += "."
				IpList.append(output[:-1])
				prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
				dpg.set_value("Vysledek_" + str(i+1), str(output[:-1]))
		else:
			dpg.set_value("Vysledek_" + str(i+1), "Zkontrolujte zadanout IP")
	list_of_IPs = IpList.copy()
	sumarization()

with dpg.window(tag="Primary Window", label="Sumarizace IPv4", width=sirka, height=vyska):

	dpg.add_group(tag="radky")
	add_radek()
	add_radek()
	with dpg.group(horizontal=True):
		dpg.add_button(label="+", tag="plus_button", callback=lambda: add_radek()) #přidá další řádek na IP
		dpg.add_button(label="-", tag="minus_button", callback=remove_radek)
		dpg.add_button(label="Count", callback=get_full_ip) #spočítá sumarizační ip adresu
		dpg.add_checkbox(label="Binární", tag="binary") #pokud checked - vypíše je v binárním tvaru

	with dpg.group(tag="Sumarizovana IP", horizontal=True):
		dpg.add_text("Sumarizovaná IP adresa: ")
		dpg.add_text(tag="VysledekSumarizace")

dpg.set_primary_window("Primary Window", True)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
