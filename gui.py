import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox
import tkinter as tk
from df import Parser
import re
from os.path import abspath
 
class GUI:

    def __init__(self, master):
        self.master = master
        master.title("Cluster Addresses")       

        
        self.frm_main = tk.Frame(master)
        self.sheet_text = tk.StringVar(self.frm_main, value='BC Master')

        self.check_var = tk.BooleanVar(value=True)

        self.cb_old = tk.Checkbutton(self.frm_main, text="New Excele Format? (.xlsx)", variable=self.check_var, onvalue=True, offvalue=False)

        self.ent_sheet = tk.Entry(self.frm_main, textvariable=self.sheet_text)
        self.addr_text = tk.StringVar(self.frm_main, value='Address')
        self.city_text = tk.StringVar(self.frm_main, value='City')
        self.prov_text = tk.StringVar(self.frm_main, value='Prov')
        self.zip_text = tk.StringVar(self.frm_main, value='Post Cd')
        
        
        self.ent_addr = tk.Entry(self.frm_main, textvariable=self.addr_text)
        self.ent_city = tk.Entry(self.frm_main, textvariable=self.city_text)
        self.ent_prov = tk.Entry(self.frm_main, textvariable=self.prov_text)
        self.ent_zip = tk.Entry(self.frm_main, textvariable=self.zip_text)

        self.start_num = tk.IntVar(self.frm_main, value=0)
        self.end_num = tk.IntVar(self.frm_main, value=50)
        self.ent_start = tk.Entry(self.frm_main, textvariable=self.start_num)
        self.ent_end = tk.Entry(self.frm_main, textvariable=self.end_num)

        self.rt_text = tk.StringVar(self.frm_main, value='RT43, RT46, RT47, RT48, RT50, RT51, RT52, RT53')
        self.ent_rt = tk.Entry(self.frm_main, textvariable=self.rt_text)
        
        self.btn_open = tk.Button(self.frm_main, text="Open", command=self.__open_file)
        self.btn_op = tk.Button(self.frm_main, text="Operate", command=self.__operate)
        self.lbl_addr = tk.Label(self.frm_main, text="Address")
        self.lbl_city = tk.Label(self.frm_main, text="City")
        self.lbl_province = tk.Label(self.frm_main, text="Province")
        self.lbl_postal = tk.Label(self.frm_main, text="Postal")
        self.lbl_routes = tk.Label(self.frm_main, text="Routes")
        self.lbl_start = tk.Label(self.frm_main, text="Start")
        self.lbl_end = tk.Label(self.frm_main, text="End")

        self.frm_main.grid(row=0, column=0, padx=10, pady=10)
        self.ent_sheet.grid(row=0, column=1)
        self.btn_open.grid(row=0, column=0, padx=5, pady=5)
        self.cb_old.grid(row=1, column=1, padx=5)
        self.lbl_addr.grid(row=2, column=0)
        self.lbl_city.grid(row=2, column=1)
        self.lbl_province.grid(row=4, column=0)
        self.lbl_postal.grid(row=4, column=1)
        self.lbl_routes.grid(row=6, column=0)
        self.lbl_start.grid(row=8, column=0)
        self.lbl_end.grid(row=8, column=1)

        self.ent_addr.grid(row=3, column=0)
        self.ent_city.grid(row=3, column=1)
        self.ent_prov.grid(row=5, column=0)
        self.ent_zip.grid(row=5, column=1)
        self.ent_rt.grid(row=7, column=0)
        self.ent_start.grid(row=9, column=0)
        self.ent_end.grid(row=9, column=1)

        self.btn_op.grid(row=10, column=0, padx=5, pady=5)



        self.parser = None


    def __open_file(self):
        sheet = self.sheet_text.get()
        new = self.check_var.get()
        if not sheet:
            messagebox.showerror("Entry Error!", "Sheet Name Not Entered")
            return


        filepath = askopenfilename(
            filetypes=[("Excel Files", "*.xls"), ("Excel 2007+ Files", "*.xlsx")]
        )
        if not filepath:
            return
        
        self.parser = Parser(abspath(filepath), sheet, new)

    def __operate(self):
        if not self.parser:
            messagebox.showerror("Object Error!", "File Not Opened Yet")
            return

        addr = self.addr_text.get()
        city = self.city_text.get()
        prov = self.prov_text.get()
        zip = self.zip_text.get()

        if not addr or not city or not prov or not zip:
            messagebox.showerror("Entry Error!", "Address, City, Province or Postal Code Not Entered")
            return

        routes = [rt.strip() for rt in self.rt_text.get().split(",")]

        rt_re = re.compile("RT\d\d")

        for route in routes:
            if not rt_re.match(route):
                messagebox.showerror("Pattern Error!", "One of the Routes Does not Match the Given Pattern (RT\d\d)")
                return

        start_num = self.start_num.get()
        end_num = self.end_num.get()

        print(start_num, end_num)

        if start_num is None or end_num is None:
            messagebox.showerror("Entry Error!", "Start Number or End Number Not Entered")
            return

        done, err = self.parser.operate(routes, addr, city, prov, zip, start_num, end_num)

        messagebox.showinfo("Done!", f"File saved in the same location as input. {done} routes saved, {err} didn't.")
