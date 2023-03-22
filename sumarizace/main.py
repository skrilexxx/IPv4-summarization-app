import dearpygui.dearpygui as dpg

class summarization:
    def __init__(self) -> None:
        self.width = 600
        self.height = 600
        self.count = 1
        self.listOfIPs = []
        self.prefixList = []


    def run(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title='Summarization IPv4', width=self.width, height=self.height)
        with dpg.window(tag="Primary Window", label="Summarization IPv4", width=self.width, height=self.height):
            dpg.add_group(tag="lines")
            self.add_line()
            self.add_line()
            with dpg.group(horizontal=True):
                dpg.add_button(label="+", tag="plus_button", callback=lambda: self.add_line()) #adds line for IP
                dpg.add_button(label="-", tag="minus_button", callback=self.remove_line) #removes line with IP
                dpg.add_button(label="Count", callback=self.get_full_ip) #counts sumarization IP address
                dpg.add_checkbox(label="Binary", tag="binary") #if checked - shows ip addresses in binary

            with dpg.group(tag="Summarized IP", horizontal=True):
                dpg.add_text("Summarized IP address: ")
                dpg.add_text(tag="SumarizationResult")

        dpg.set_primary_window("Primary Window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def limit(sender, app_data, user_data):
        """Limits input 0-255 - does not work right now"""
        if app_data != "":
            if int(app_data) < 0:
                dpg.set_value(sender, "0")
            elif int(app_data) > 255:
                dpg.set_value(sender, "255")
        elif len(app_data) > user_data:
            dpg.set_value(sender, app_data[:user_data])

    def add_line(self) -> None:
        """Adds line for IP"""
        with dpg.group(tag="line_" + str(self.count), horizontal=True, parent="lines"):
            dpg.add_text("IP address:")
            dpg.add_input_text(hint="***", width=30, tag=f"IP_{self.count}_1", decimal=True, callback=self.limit, user_data=3) #IP_1 (- první IP) _1 (- část IP 1-5, 5= prefix)
            dpg.add_text(".")
            dpg.add_input_text(hint="***", width=30, tag=f"IP_{self.count}_2", decimal=True, callback=self.limit, user_data=3)
            dpg.add_text(".")
            dpg.add_input_text(hint="***", width=30, tag=f"IP_{self.count}_3", decimal=True, callback=self.limit, user_data=3)
            dpg.add_text(".")
            dpg.add_input_text(hint="***", width=30, tag=f"IP_{self.count}_4", decimal=True, callback=self.limit, user_data=3)
            dpg.add_text("/")
            dpg.add_input_text(hint="**", width=20, tag=f"IP_{self.count}_5", decimal=True, callback=self.limit, user_data=2)

            dpg.add_text(tag="Result_" + str(self.count))

        dpg.set_value("Result_" + str(self.count), "")
        self.count += 1

    def remove_line(self) -> None:
        """Deletes last line"""
        if self.count > 3:
            self.count -= 1
            dpg.delete_item("line_" + str(self.count))

    def min_max(listIp, List) -> list[str]:
        """Finds biggest[0] a smallest[1] IP address and smallest prefix """
        return [max(listIp), min(listIp), min(List)]

    def ip_sumarization(self):
        """Counts summarization IP address"""
        BigSmallIp = self.min_max(self.listOfIPs, self.prefixList)
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

        dpg.set_value("SummarizationResult", sumIp[:-1] + " / " + str(finalPrefix))


    def get_full_ip(self):
        """Gets full IP address from input, v D and B"""
        self.prefixList.clear()
        self.listOfIPs.clear()
        IpList = []
        for i in range(self.count-1):
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
                    self.prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
                    dpg.set_value("Result_" + str(i+1), outputBin[:-1])
                else:
                    for x in range(4):
                        output += str(dpg.get_value("IP_"+ str(i+1) +"_" + str(x+1)))
                        output += "."
                    IpList.append(output[:-1])
                    self.prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
                    dpg.set_value("Result_" + str(i+1), str(output[:-1]))
            else:
                dpg.set_value("Result_" + str(i+1), "Zkontrolujte zadanout IP")
        self.listOfIPs= IpList.copy()
        self.ip_sumarization()



w1 = summarization()
w1.run()