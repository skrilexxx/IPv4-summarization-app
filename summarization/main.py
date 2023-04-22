import dearpygui.dearpygui as dpg
from os import sep, path
import sys

class Summarization:
    def __init__(self) -> None:
        self.width = 625
        self.height = 625
        self.count = 1
        self.listOfIPs = []
        self.prefixList = []
        self.edge = 0
        self.finalPrefix = 0
        self.sumBinIp = ""
        self.sumIp = ""

        if getattr(sys, 'frozen', False):
            self.app_path = sys._MEIPASS
        else:
            self.app_path = path.dirname(path.abspath(__file__))

    def relpath(self, path: str) -> str:
        return self.app_path + sep + path.replace("/", sep)

    def run(self) -> None:
        dpg.create_context()
        dpg.create_viewport(title='Summarization IPv4', width=self.width, height=self.height, small_icon=self.relpath("icon.ico"), large_icon=self.relpath("icon.ico"), min_height=250, min_width=self.width)
        with dpg.window(tag="Primary Window", label="Summarization IPv4", width=self.width, height=self.height):
            dpg.add_group(tag="lines")
            self.add_line()
            self.add_line()
            with dpg.group(horizontal=True):
                dpg.add_button(label="+", tag="plus_button", callback=lambda: self.add_line()) #adds line for IP
                dpg.add_button(label="-", tag="minus_button", callback=self.remove_line) #removes line with IP
                dpg.add_button(label="Count", callback=self.ip_summarization) #counts sumarization IP address
                dpg.add_checkbox(label="Binary", tag="binary") #if checked - shows ip addresses in binary

            with dpg.group(tag="Summarized IP", horizontal=True):
                dpg.add_text("Summarized IP address:")
                dpg.add_text(tag="SummarizationResult")

        dpg.set_primary_window("Primary Window", True)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def limit(self, sender, app_data, user_data):
        """Limits input 0-255"""
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

    def min_max(self, listIp, prefList) -> list[str]:
        """Finds biggest[0] a smallest[1] IP address and smallest prefix """
        return [max(listIp), min(listIp), min(prefList)]

    def ip_summarization(self):
        """Counts summarization IP address"""
        self.get_full_ip()
        BigSmallIp = self.min_max(self.listOfIPs, self.prefixList)

        max = BigSmallIp[0].split(".")
        min = BigSmallIp[1].split(".")
        prefix = BigSmallIp[2]
        sumZeros = 0
        maxPrefix = 32
        self.finalPrefix = 0
        self.edge = 0

        maxBin = []
        minBin = []
        sumBin = []
        self.sumBinIp = ""
        self.sumIp = ""
        same = True

        for i in range(len(max)):
            maxBin.append(bin(int(max[i]))[2:].zfill(8))
            minBin.append(bin(int(min[i]))[2:].zfill(8))

        for i in range(len(maxBin)):

            sumSeg = ""
            for y in range(len(maxBin[i])):
                if same and maxBin[i][y] == minBin[i][y]:
                    sumSeg = sumSeg + str(maxBin[i][y])
                    self.edge += 1
                else:
                    same = False
                if same == False:
                    sumSeg = sumSeg + "0"
                    sumZeros += 1
            sumBin.append(sumSeg)

        if (maxPrefix-sumZeros) == prefix:
            self.finalPrefix = prefix
        elif (maxPrefix-sumZeros) > prefix:
            self.finalPrefix = prefix
        else:
            self.finalPrefix = (maxPrefix-sumZeros)

        for number in sumBin:
            self.sumIp += str(int(number, 2))+"."
            self.sumBinIp += str(number)+"."
        self.show_edge()

    def get_full_ip(self):
        """Gets full IP address from input, v D and B"""
        self.prefixList.clear()
        self.listOfIPs.clear()
        IpList = []
        for i in range(self.count-1):
            output = ""
            if ((dpg.get_value("IP_"+ str(i+1) +"_1") != "") and  (dpg.get_value("IP_"+ str(i+1) +"_4") != "") and (dpg.get_value("IP_"+ str(i+1) +"_5") != "")):
                    for x in range(4):
                        output += str(dpg.get_value("IP_"+ str(i+1) +"_" + str(x+1)))
                        output += "."
                    IpList.append(output[:-1])
                    self.prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
                    dpg.set_value("Result_" + str(i+1), "")
            else:
                dpg.set_value("Result_" + str(i+1), "Check entered IP")
        self.listOfIPs= IpList.copy()

    def show_edge(self):
        """Prints IP addresses i D and B - in B shows edge"""
        for i in range(self.count-1):
            output = ""
            outputBinHelp = ""
            outputBin = ""
            edge_done = False
            edgeHelp = self.edge

            if ((dpg.get_value("IP_"+ str(i+1) +"_1") != "") and  (dpg.get_value("IP_"+ str(i+1) +"_4") != "") and (dpg.get_value("IP_"+ str(i+1) +"_5") != "")):
                if dpg.get_value("binary"):
                    for y in range(4):
                        outputBinHelp += str(bin(int(dpg.get_value("IP_"+ str(i+1) +"_" + str(y+1))))[2:]).zfill(8)
                        outputBinHelp += "."

                    for bit in outputBinHelp:
                            if bit != ".":
                                if edgeHelp == 0 and edge_done == False:
                                    outputBin += " | "
                                    outputBin += str(bit)
                                    edge_done = True
                                else:
                                    edgeHelp -= 1
                                    outputBin += str(bit)
                            elif bit == ".":
                                outputBin += str(bit)
                            else:
                                outputBin = "Error"

                    self.prefixList.append(int(dpg.get_value("IP_"+ str(i+1) +"_5")))
                    dpg.set_value("Result_" + str(i+1), outputBin[:-1])

            else:
                dpg.set_value("Result_" + str(i+1), "Check entered IP")
        self.summarization_output()

    def summarization_output(self):
        edge_done = False
        edgeHelp = self.edge
        sumBinIpFinal = ""

        if dpg.get_value("binary"):
            for bit in self.sumBinIp:
                    if bit != ".":
                        if edgeHelp == 0 and edge_done == False:
                            sumBinIpFinal += " | "
                            sumBinIpFinal += str(bit)
                            edge_done = True
                        else:
                            edgeHelp -= 1
                            sumBinIpFinal += str(bit)
                    elif bit == ".":
                        sumBinIpFinal += str(bit)
                    else:
                        sumBinIpFinal = "Error"
            dpg.set_value("SummarizationResult", self.sumIp[:-1] + " / " + str(self.finalPrefix) + "   B: " + sumBinIpFinal[:-1])
        else:
            dpg.set_value("SummarizationResult", self.sumIp[:-1] + " / " + str(self.finalPrefix))




w1 = Summarization()
w1.run()