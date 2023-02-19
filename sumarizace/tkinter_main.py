from tkinter import *

def calculate():
	ip1=entry1.get()
	ip2=entry2.get()

	if(ip2 == "" or ip1==""):
		messagebox.showinfo("", "Enter two IP address at least")

	else:
		messagebox.showinfo("", ip1+ip2)


root= Tk()
root.title("Substituce IPv4")
root.geometry("400x300")

global entry1
global entry2
Label(root, text="Sumarizace IPv4 ").place(x=150,y=0)
Label(root, text="Enter IP address:").place(x=20,y=20)
Label(root, text="Enter IP address:").place(x=20,y=40)

#prvni Ip
entry1a=Entry(root, width=5)
entry1a.place(x=140, y=20)
Label(root, text=".").place(x=170,y=20)
entry1b=Entry(root, width=5)
entry1b.place(x=180, y=20)
Label(root, text=".").place(x=210,y=20)
entry1c=Entry(root, width=5)
entry1c.place(x=220,y=20)
Label(root, text=".").place(x=250,y=20)
entry1d=Entry(root, width=5)
entry1d.place(x=260, y=20)
Label(root, text="/").place(x=300,y=20)
entry1f=Entry(root, width=3)
entry1f.place(x=310, y=20)

#druha ip
entry2a=Entry(root, width=5)
entry2a.place(x=140, y=40)
Label(root, text=".").place(x=170,y=40)
entry2b=Entry(root, width=5)
entry2b.place(x=180, y=40)
Label(root, text=".").place(x=210,y=40)
entry2c=Entry(root, width=5)
entry2c.place(x=220,y=40)
Label(root, text=".").place(x=250,y=40)
entry2d=Entry(root, width=5)
entry2d.place(x=260, y=40)
Label(root, text="/").place(x=300,y=40)
entry2f=Entry(root, width=3)
entry2f.place(x=310, y=40)



Button(root, text="Calculate", command=calculate, height=1, width=13).place(x=150, y=120)
root.mainloop()