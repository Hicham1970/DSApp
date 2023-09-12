import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from PIL.ImageQt import rgb
from tkcalendar import DateEntry
import os
import random
import tempfile
import smtplib
from tkinter import font


class FirstPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.SecondPage = None

        load = Image.open("login.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        pg1_lbl = Label(self, text='Username', fg="white",
                        font=('Arial', 15, 'bold'),
                        background='#00192c')
        pg1_lbl.place(x=850, y=400)
        pg1_entry = Entry(self,
                          font=('Arial', 15, 'bold'), width=20)
        pg1_entry.place(x=980, y=400)

        pg1_lbl2 = Label(self,
                         text='Password', fg="white",
                         font=('Arial', 15, 'bold'),
                         background='#00192c')
        pg1_lbl2.place(x=850, y=450)
        pg1_entry2 = Entry(self, font=('Arial', 15, 'bold'), show='*', width=20)
        pg1_entry2.place(x=980, y=450)

        # lbl = tk.Label(border, text='FirstPage', bg='ivory', font=('Arial', 12, 'bold'))
        # lbl.place(x=22, y=23)

        def verify():
            with open("credentials.txt", "r") as f:
                info = f.readlines()
                i = 0
                for e in info:
                    u, p = e.split(",")
                    if u.strip() == pg1_entry.get() and p.strip() == pg1_entry2.get():
                        controller.show_frame(SecondPage)
                        i = 1
                        break
                if i == 0:
                    messagebox.showerror('Error', 'Please provide a registered'
                                                  ' credentials or register now to get access to the application')

        btn1 = tk.Button(self, background='orange', fg='#00192c', text='Submit', font=('Arial', 16, 'bold'),
                         command=verify)
        btn1.place(x=910, y=520)

        def register():
            window = tk.Tk()
            window.geometry('500x250+0+0')
            window.resizable(False, False)
            window.title('Register')

            canvas = tk.LabelFrame(window, text='Registration panel', fg='gold', font=('Arial', 16, 'bold'), bd=5,
                                   bg='#00192c')
            canvas.pack(expand=True, fill='both')

            l1 = tk.Label(canvas, text='Username', fg='orange', font=('Arial', 14, 'bold'), bg='#00192c')
            l1.place(x=10, y=10, )
            ent1 = tk.Entry(canvas, width=30, bd=5)
            ent1.place(x=200, y=10)
            l2 = tk.Label(canvas, text='Password', fg='orange', font=('Arial', 14, 'bold'), bg='#00192c')
            l2.place(x=10, y=60)
            ent2 = tk.Entry(canvas, show='*', width=30, bd=5)
            ent2.place(x=200, y=60)
            l3 = tk.Label(canvas, text='Confirm Password', fg='orange', font=('Arial', 14, 'bold'), bg='#00192c')
            l3.place(x=10, y=110)
            ent3 = tk.Entry(canvas, show='*', width=30, bd=5)
            ent3.place(x=200, y=110)

            def check():
                if ent1.get() != '' or ent2.get() != '' or ent3.get() != '':
                    if ent2.get() == ent3.get():
                        with open("credentials.txt", "a") as f:
                            f.write(ent1.get() + "," + ent2.get() + "\n")
                            messagebox.showinfo("Welcome", "you are registered successfully")
                    else:
                        messagebox.showerror('Error', 'Your password did not match')
                else:
                    messagebox.showerror('Error', 'please fill the complete fields')

            btn = tk.Button(canvas, text='Sign In', bg='orange', font=('Arial', 16, 'bold'), command=check)
            btn.place(x=306, y=160)

        btn2 = tk.Button(self, text='Register', cursor='hand2', background='orange', font=('Arial', 16, 'bold'),
                         command=register)
        btn2.place(x=980, y=30)


class SecondPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        # attaching the ThirdPage to this page
        self.ThirdPage = None

        draft_number: int = random.randint(234, 7645)


        load = Image.open("login.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        # lbl = tk.Label(self, text='SecondPage', font=('Arial', 12, 'bold'))
        # lbl.place(x=222, y=

        self.frame_content = ttk.Frame(self)

        # frame1
        self.title_lbl = tk.Label(self,
                                  text='Initial Draft survey',
                                  bd=6,
                                  font=('arial', 14, 'bold'),
                                  relief='groove',
                                  background='gray12',
                                  fg='gold')
        self.title_lbl.pack(side='top', fill='x')

        frm = tk.LabelFrame(self,
                            font=('times new roman', 12, 'bold'),
                            background='gray12',
                            fg='gold',
                            text='Operation Information', bd=6, relief='groove')
        frm.pack(side='top', fill='both')
        # Labels:
        self.vessel_lbl = tk.Label(
            frm, text="Vessel", foreground='gold', background='gray12')
        self.flag_lbl = tk.Label(
            frm, text="Flag:", background='gray12', foreground='gold', anchor='e')
        self.registry_lbl = tk.Label(
            frm, text="Registry:", background='gray12', foreground='gold', anchor='e')
        self.imo_lbl = tk.Label(
            frm, text="Imo:", background='gray12', foreground='gold', anchor='e')
        self.Cargo_lbl = tk.Label(
            frm, text="Cargo", background='gray12', foreground='gold', anchor='e')
        self.Client_lbl = tk.Label(
            frm, text="client", background='gray12', foreground='gold', anchor='e')
        self.quantity_lbl = tk.Label(
            frm, text="Quantity BL", foreground='gold', background='gray12', anchor='e')
        self.load_port_lbl = tk.Label(
            frm, text="Loading Port", foreground='gold', background='gray12', anchor='e')
        self.disch_port_lbl = tk.Label(
            frm, text="Discharging Port", background='gray12', foreground='gold', anchor='e')
        self.arrival_lbl = tk.Label(
            frm, text="Arrival", background='gray12', foreground='gold', anchor='e')
        self.birthing_lbl = tk.Label(
            frm, text="Birthing time", foreground='gold', background='gray12', anchor='e')
        self.survey_lbl = tk.Label(
            frm, text="Initial DS", background='gray12', foreground='gold', anchor='e')
        self.arrival_time_lbl = tk.Label(
            frm, text="Time", background='gray12', foreground='gold', anchor='e')
        self.birthing_time_lbl = tk.Label(
            frm, text="Time", foreground='gold', background='gray12', anchor='e')
        self.survey_time_lbl = tk.Label(
            frm, text="Time", foreground='gold', background='gray12', anchor='e')

        self.draft_number_lbl = tk.Label(
            frm, text="Draft N°:", foreground='gold',
            font=('times new roman', 8),
            background='gray12', anchor='w')

        # entries
        self.vessel_entry = tk.Entry(
            frm, width=22, background='gray80', font=('times new roman', 10, 'bold'))
        self.flag_entry = tk.Entry(
            frm, width=22, background='gray80', font=('times new roman', 10, 'bold'))
        self.registry_entry = tk.Entry(
            frm, width=22, background='gray80', font=('times new roman', 10, 'bold'))
        self.imo_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))
        self.cargo_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))
        self.client_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))
        self.quantity_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))
        self.load_port_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))
        self.disch_port_entry = tk.Entry(
            frm, width=16, background='gray80', font=('times new roman', 10, 'bold'))

        self.cal1 = DateEntry(frm, width=7, selectmode='day', background='gray80', font=(
            'times new roman', 10, 'bold'))
        self.cal2 = DateEntry(frm, width=7, selectmode='hour', background='gray80',
                              font=('times new roman', 10, 'bold'))
        self.cal3 = DateEntry(frm, width=7, background='gray80', font=(
            'times new roman', 10, 'bold'))
        self.arrival_time = tk.Entry(
            frm, width=6, background='gray80', font=('times new roman', 10, 'bold'))
        self.birthing_time = tk.Entry(
            frm, width=6, background='gray80', font=('times new roman', 10, 'bold'))
        self.initialds_time = tk.Entry(
            frm, width=6, background='gray80', font=('times new roman', 10, 'bold'))
        self.header_btn = tk.Button(frm,
                                    text='Data',
                                    foreground='snow',
                                    bg='black',
                                    width=8, command=self.save_data)
        self.search_btn = tk.Button(frm,
                                    text='Search',
                                    foreground='snow',
                                    bg='black',
                                    width=8,
                                    command=self.search_data)
        self.print_btn = tk.Button(frm,
                                   text='Print',
                                   foreground='snow',
                                   bg='black',
                                   width=8,
                                   command=self.print)

        self.radio_var = tk.StringVar()
        self.operation_loading = tk.Radiobutton(frm, text='Loading',
                                                font=('times new roman',
                                                      10, 'bold'),
                                                background='gray12', fg='gold',
                                                value='load', variable=self.radio_var,
                                                width=5, command=self.choice)

        self.operation_discharging = tk.Radiobutton(frm, text='Discharge', font=('times new roman', 10, 'bold'),
                                                    background='gray12', fg='gold',
                                                    value='discharge', variable=self.radio_var,
                                                    command=self.choice)
        self.draft_number_entry = tk.Entry(frm, width=10)
        # Layout
        self.vessel_lbl.grid(row=0, column=0, pady=3, padx=0)
        self.flag_lbl.grid(row=1, column=0, pady=3, padx=0)
        self.registry_lbl.grid(row=2, column=0, pady=3, padx=0)
        self.imo_lbl.grid(row=0, column=2, pady=3, padx=0)
        self.Cargo_lbl.grid(row=1, column=2, pady=3, padx=0)
        self.Client_lbl.grid(row=2, column=2, pady=3, padx=0)
        self.quantity_lbl.grid(row=0, column=4, pady=3, padx=0)
        self.load_port_lbl.grid(row=1, column=4, pady=3, padx=0)
        self.disch_port_lbl.grid(row=2, column=4, pady=3, padx=0)
        self.arrival_lbl.grid(row=0, column=6, pady=3, padx=0)
        self.birthing_lbl.grid(row=1, column=6, pady=3, padx=0)
        self.survey_lbl.grid(row=2, column=6, pady=3, padx=0)
        self.arrival_time_lbl.grid(row=0, column=8, pady=3, padx=5)
        self.birthing_time_lbl.grid(row=1, column=8, pady=3, padx=5)
        self.survey_time_lbl.grid(row=2, column=8, pady=3, padx=5)
        self.draft_number_lbl.grid(row=2, column=12, pady=3, padx=5)

        self.vessel_entry.grid(row=0, column=1, pady=3, padx=0)
        self.flag_entry.grid(row=1, column=1, pady=3, padx=0)
        self.registry_entry.grid(row=2, column=1, pady=3, padx=0)
        self.imo_entry.grid(row=0, column=3, pady=3, padx=0)
        self.cargo_entry.grid(row=1, column=3, pady=3, padx=0)
        self.client_entry.grid(row=2, column=3, pady=3, padx=0)
        self.quantity_entry.grid(row=0, column=5, pady=3, padx=0)
        self.load_port_entry.grid(row=1, column=5, pady=3, padx=0)
        self.disch_port_entry.grid(row=2, column=5, pady=3, padx=0)
        self.cal1.grid(row=0, column=7, pady=3, padx=0)
        self.cal2.grid(row=1, column=7, pady=3, padx=0)
        self.cal3.grid(row=2, column=7, pady=3, padx=0)
        self.arrival_time.grid(row=0, column=9, pady=3, padx=3)
        self.birthing_time.grid(row=1, column=9, pady=3, padx=3)
        self.initialds_time.grid(row=2, column=9, pady=3, padx=3)
        self.header_btn.grid(row=0, column=13, pady=3, padx=3)
        self.search_btn.grid(row=0, column=14, pady=3, padx=3)
        self.print_btn.grid(row=2, column=14, pady=3, padx=3)

        self.operation_loading.grid(row=1, column=13, pady=3, padx=3)
        self.operation_discharging.grid(row=1, column=14, pady=3)
        self.draft_number_entry.grid(row=2, column=13, pady=3)
        # "

        frame = tk.LabelFrame(self, bd=6,
                              font=('times new roman', 12, 'bold'), background='gray12', fg='gold',
                              text='Input Observation', relief='groove', width=600, height=800)
        frame.pack(side='left', fill='both')
        # labels
        self.lbp_lbl = tk.Label(
            frame, text="LBP", foreground='gold', background='gray12')
        self.draft_for_lbl = tk.Label(
            frame, text="Draft For:", foreground='gold', anchor='w', background='gray12')
        self.draft_aft_lbl = tk.Label(
            frame, text="Draft Aft:", foreground='gold', anchor='e', background='gray12')
        self.draft_mid_lbl = tk.Label(
            frame, text="Draft Mid:", foreground='gold', anchor='e', background='gray12')
        self.portside_lbl = tk.Label(
            frame, text="Port side", foreground='gold', anchor='e', background='gray12')
        self.starboard_lbl = tk.Label(
            frame, text="Starboard", foreground='gold', anchor='e', background='gray12')
        self.distance_lbl = tk.Label(
            frame, text="Distance", foreground='gold', anchor='e', background='gray12')
        self.position_lbl = tk.Label(
            frame, text="Position", foreground='gold', anchor='e', background='gray12')

        self.obs_trim_lbl = tk.Label(
            frame, text="Obs.Trim:", state='normal', foreground='gold', anchor='e', background='gray12')
        self.lbm_lbl = tk.Label(
            frame, text="Lbm:", foreground='gold', anchor='e', background='gray12')
        self.corrected_for_lbl = tk.Label(
            frame, text="Draft For Cor:", foreground='gold', anchor='e', background='gray12')
        self.corrected_aft_lbl = tk.Label(
            frame, text="Draft Aft Cor:", foreground='gold', anchor='e', background='gray12')
        self.corrected_mid_lbl = tk.Label(
            frame, text="Draft Mid cor:", foreground='gold', anchor='e', background='gray12')
        self.mean_for_aft_lbl = tk.Label(
            frame, text="MFA:", state='normal', foreground='gold', anchor='e', background='gray12')
        self.mean_of_mean_lbl = tk.Label(
            frame, text="MOM:", state='normal', foreground='gold', anchor='e', background='gray12')
        self.quarter_mean_lbl = tk.Label(
            frame, text="QM:", state='normal', foreground='gold', anchor='e', background='gray12')
        self.result_lbl = tk.Label(
            frame, text="", foreground='gold', anchor='w', background='gray12')

        # entries
        self.lbp_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                  fg="wheat1")
        self.draft_for_port_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.draft_for_star_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.draft_aft_port_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.draft_aft_star_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.draft_mid_port_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.draft_mid_star_entry = tk.Entry(frame, width=6, background='gray37', font=('times new roman', 10, 'bold'),
                                             fg="wheat1")
        self.distance_from_for_pp_entry = tk.Entry(frame, width=6, background='gray37',
                                                   font=('times new roman', 10, 'bold'), fg="wheat1")
        self.distance_from_aft_pp_entry = tk.Entry(frame, width=6, background='gray37',
                                                   font=('times new roman', 10, 'bold'), fg="wheat1")
        self.distance_from_mid_pp_entry = tk.Entry(frame, width=6, background='gray37',
                                                   font=('times new roman', 10, 'bold'), fg="wheat1")

        self.position_from_for_pp_combobox = ttk.Combobox(
            frame, values=["A", "F", "N/A"], width=4)
        self.position_from_aft_pp_combobox = ttk.Combobox(
            frame, values=["A", "F", "N/A"], width=4)
        self.position_from_mid_pp_combobox = ttk.Combobox(
            frame, values=["A", "F", "N/A"], width=4)

        self.obs_trim_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                       fg="aquamarine2")
        self.lbm_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                  fg="aquamarine2")
        self.corrected_for_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                            fg="aquamarine2")
        self.corrected_aft_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                            fg="aquamarine2")
        self.corrected_mid_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                            fg="aquamarine2")
        self.mean_for_aft_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                           fg="aquamarine2")
        self.mean_of_mean_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                           fg="aquamarine2")
        self.quarter_mean_entry = tk.Entry(frame, width=8, background='gray37', font=('times new roman', 10, 'bold'),
                                           fg="aquamarine2")

        self.button_entry = tk.Button(frame, text='Calculate',
                                      foreground='snow',
                                      bg='black',
                                      command=self.calculate_values)

        # Layout
        self.lbp_lbl.grid(row=0, column=0, pady=12, padx=0)
        self.draft_for_lbl.grid(row=2, column=0, pady=3, padx=0)
        self.draft_aft_lbl.grid(row=3, column=0, pady=3, padx=0)
        self.draft_mid_lbl.grid(row=4, column=0, pady=3, padx=0)
        self.portside_lbl.grid(row=1, column=1, pady=3, padx=0)
        self.starboard_lbl.grid(row=1, column=2, pady=3, padx=0)
        self.distance_lbl.grid(row=1, column=3, pady=3, padx=0)
        self.position_lbl.grid(row=1, column=4, pady=3, padx=0)
        self.result_lbl.grid(row=9, column=2, pady=3, padx=0)

        self.lbp_entry.grid(row=0, column=1, pady=12, padx=3)
        self.draft_for_port_entry.grid(row=2, column=1, pady=3, padx=0)
        self.draft_for_star_entry.grid(row=2, column=2, pady=3, padx=0)
        self.draft_aft_port_entry.grid(row=3, column=1, pady=3, padx=0)
        self.draft_aft_star_entry.grid(row=3, column=2, pady=3, padx=0)
        self.draft_mid_port_entry.grid(row=4, column=1, pady=3, padx=0)
        self.draft_mid_star_entry.grid(row=4, column=2, pady=3, padx=0)
        self.distance_from_for_pp_entry.grid(row=2, column=3, pady=3, padx=2)
        self.distance_from_aft_pp_entry.grid(row=3, column=3, pady=3, padx=2)
        self.distance_from_mid_pp_entry.grid(row=4, column=3, pady=3, padx=2)
        self.position_from_for_pp_combobox.grid(
            row=2, column=4, pady=3, padx=0)
        self.position_from_aft_pp_combobox.grid(
            row=3, column=4, pady=3, padx=0)
        self.position_from_mid_pp_combobox.grid(
            row=4, column=4, pady=3, padx=0)

        self.obs_trim_lbl.grid(row=5, column=0, pady=12, padx=0)
        self.lbm_lbl.grid(row=5, column=2, pady=12, padx=0)
        self.corrected_for_lbl.grid(row=6, column=0, pady=3, padx=0)
        self.corrected_aft_lbl.grid(row=7, column=0, pady=3, padx=0)
        self.corrected_mid_lbl.grid(row=8, column=0, pady=3, padx=0)
        self.mean_for_aft_lbl.grid(row=6, column=2, pady=3, padx=0)
        self.mean_of_mean_lbl.grid(row=7, column=2, pady=3, padx=0)
        self.quarter_mean_lbl.grid(row=8, column=2, pady=3, padx=0)
        self.result_lbl.grid(row=9, column=1, pady=3, padx=0)

        self.obs_trim_entry.grid(row=5, column=1, pady=12, padx=0)
        self.lbm_entry.grid(row=5, column=3, pady=12, padx=0)
        self.corrected_for_entry.grid(row=6, column=1, pady=3, padx=0)
        self.corrected_aft_entry.grid(row=7, column=1, pady=3, padx=0)
        self.corrected_mid_entry.grid(row=8, column=1, pady=3, padx=0)
        self.mean_for_aft_entry.grid(row=6, column=3, pady=3, padx=0)
        self.mean_of_mean_entry.grid(row=7, column=3, pady=3, padx=0)
        self.quarter_mean_entry.grid(row=8, column=3, pady=3, padx=0)
        self.button_entry.grid(row=9, column=0, pady=5, padx=1)

        self.obs_trim_entry.configure(state=DISABLED)
        self.lbm_entry.configure(state=DISABLED)
        self.corrected_for_entry.configure(state=DISABLED)
        self.corrected_aft_entry.configure(state=DISABLED)
        self.corrected_mid_entry.configure(state=DISABLED)
        self.mean_for_aft_entry.configure(state=DISABLED)
        self.mean_of_mean_entry.configure(state=DISABLED)
        self.quarter_mean_entry.configure(state=DISABLED)

        # frame2 = tk.Frame(self, bd=6, relief='groove', height=200)
        # frame2.pack(side='left', fill='y')

        self.draft_sup_lbl = tk.Label(
            frame, text="Draft Sup:", foreground='gold', background='gray12')
        self.draft_inf_lbl = tk.Label(
            frame, text="Draft Inf:", foreground='gold', background='gray12')
        self.init_draft_lbl = tk.Label(
            frame, text="Initial Draft:", foreground='gold', background='gray12')
        self.displacement_lbl = tk.Label(
            frame, text="Disp", foreground='gold', background='gray12')
        self.tpc_lbl = tk.Label(
            frame, text="TPC", foreground='gold', background='gray12')
        self.lcf_lbl = tk.Label(
            frame, text="LCF", foreground='gold', background='gray12')
        self.draft_lbl = tk.Label(
            frame, text="Draft", foreground='gold', background='gray12')
        self.text_lbl = tk.Label(
            frame, text="", foreground='gold', background='gray12')

        self.draft_sup_entry = tk.Entry(
            frame, width=7, background='gray37', font=('times new roman', 10, 'bold'))
        self.init_draft_entry = tk.Entry(
            frame, width=7, background='gray37', font=('times new roman', 10, 'bold'))
        self.draft_inf_entry = tk.Entry(
            frame, width=7, background='gray37', font=('times new roman', 10, 'bold'))
        self.displacement_sup_entry = tk.Entry(frame, width=7, background='gray37',
                                               font=('times new roman', 10, 'bold'))
        self.init_displacement_entry = tk.Entry(
            frame, width=7, state='normal', background='gray37', font=('times new roman', 10, 'bold'))
        self.displacement_inf_entry = tk.Entry(frame, width=7, background='gray37',
                                               font=('times new roman', 10, 'bold'))
        self.tpc_sup_entry = tk.Entry(
            frame, width=7, background='gray37', font=('times new roman', 10, 'bold'))
        self.init_tpc_entry = tk.Entry(frame, width=7, state='normal', background='gray37',
                                       font=('times new roman', 10, 'bold'))
        self.tpc_inf_entry = tk.Entry(
            frame, width=7, background='gray37', font=('times new roman', 10, 'bold'))
        self.lcf_sup_entry = tk.Entry(
            frame, width=5, background='gray37', font=('times new roman', 10, 'bold'))
        self.init_lcf_entry = tk.Entry(frame, width=5, state='normal', background='gray37',
                                       font=('times new roman', 10, 'bold'))
        self.lcf_inf_entry = tk.Entry(
            frame, width=5, background='gray37', font=('times new roman', 10, 'bold'))

        # Create the interpolation button
        self.interpolation_button = tk.Button(
            frame, text="Interpolate",
            foreground='snow',
            bg='black',
            command=self.calculate_interpolation)

        # Layout
        self.draft_sup_lbl.grid(row=12, column=0, pady=7, padx=1)
        self.init_draft_lbl.grid(row=13, column=0, pady=7, padx=1)
        self.draft_inf_lbl.grid(row=14, column=0, pady=7, padx=1)
        self.draft_lbl.grid(row=11, column=1, pady=7, padx=1)
        self.displacement_lbl.grid(row=11, column=2, pady=7, padx=1)
        self.tpc_lbl.grid(row=11, column=3, pady=7, padx=1)
        self.lcf_lbl.grid(row=11, column=4, pady=7, padx=1)
        self.text_lbl.grid(row=11, column=1, pady=7)

        self.draft_sup_entry.grid(row=12, column=1, pady=7, padx=1)
        self.init_draft_entry.grid(row=13, column=1, pady=7, padx=1)
        self.draft_inf_entry.grid(row=14, column=1, pady=7, padx=1)
        self.displacement_sup_entry.grid(row=12, column=2, pady=7, padx=1)
        self.init_displacement_entry.grid(row=13, column=2, pady=7, padx=1)
        self.displacement_inf_entry.grid(row=14, column=2, pady=7, padx=1)
        self.tpc_sup_entry.grid(row=12, column=3, pady=7, padx=1)
        self.init_tpc_entry.grid(row=13, column=3, pady=7, padx=1)
        self.tpc_inf_entry.grid(row=14, column=3, pady=7, padx=1)
        self.lcf_sup_entry.grid(row=12, column=4, pady=7, padx=1)
        self.init_lcf_entry.grid(row=13, column=4, pady=7, padx=1)
        self.lcf_inf_entry.grid(row=14, column=4, pady=7, padx=1)
        self.interpolation_button.grid(row=16, column=0, pady=7, padx=1)

        self.quarter_mean_entry.configure(state=DISABLED)
        self.init_draft_entry.configure(state=DISABLED)
        self.init_displacement_entry.configure(state=DISABLED)
        self.init_tpc_entry.configure(state=DISABLED)
        self.init_lcf_entry.configure(state=DISABLED)

        # frame3
        frame3 = tk.LabelFrame(self,
                               font=('times new roman', 12, 'bold'), background='gray12', fg='gold',
                               text='Details & Deductibles', bd=6, relief='groove')
        frame3.pack(side='left', fill='both')
        # Mtc Plus 50
        self.d_plus50_sup_lbl = tk.Label(
            frame3, text="D+50Sup:", foreground='gold', background='gray12')
        self.d_plus50_inf_lbl = tk.Label(
            frame3, text="D+50Inf:", foreground='gold', background='gray12')
        self.d_plus50_lbl = tk.Label(
            frame3, text="Draft+50:", foreground='gold', background='gray12')
        self.draft_lbl = tk.Label(
            frame3, text="Draft", foreground='gold', background='gray12')
        self.mtc1_lbl = tk.Label(
            frame3, text="MTC+", foreground='gold', background='gray12')

        self.d_plus50_sup_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.d_plus50_inf_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.d_plus50_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc_plus50_sup_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc_plus50_inf_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc1_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')

        # Layout
        self.d_plus50_sup_lbl.grid(row=1, column=0, padx=1, pady=3)
        self.d_plus50_inf_lbl.grid(row=3, column=0, padx=1, pady=3)
        self.d_plus50_lbl.grid(row=2, column=0, padx=1, pady=3)
        self.draft_lbl.grid(row=0, column=1, padx=1, pady=3)
        self.mtc1_lbl.grid(row=0, column=2, padx=1, pady=3)

        self.d_plus50_sup_entry.grid(row=1, column=1, padx=1, pady=3)
        self.d_plus50_inf_entry.grid(row=3, column=1, padx=1, pady=3)
        self.d_plus50_entry.grid(row=2, column=1, padx=1, pady=3)
        self.mtc_plus50_sup_entry.grid(row=1, column=2, padx=1, pady=3)
        self.mtc_plus50_inf_entry.grid(row=3, column=2, padx=1, pady=3)
        self.mtc1_entry.grid(row=2, column=2, padx=1, pady=3)

        # Mtc Moins 50
        self.d_moins50_sup_lbl = tk.Label(
            frame3, text="D-50Sup:", foreground='gold', background='gray12')
        self.d_moins50_inf_lbl = tk.Label(
            frame3, text="D-50Inf:", foreground='gold', background='gray12')
        self.d_moins50_lbl = tk.Label(
            frame3, text="Draft-50:", foreground='gold', background='gray12')
        self.draft_lbl = tk.Label(
            frame3, text="Draft", foreground='gold', background='gray12')
        self.mtc2_lbl = tk.Label(
            frame3, text="MTC-", foreground='gold', background='gray12')
        self.delta_mtc_lbl = tk.Label(
            frame3, text="Delta MTC", foreground='gold', background='gray12')

        self.d_moins50_sup_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.d_moins50_inf_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.d_moins50_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc_moins50_sup_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc_moins50_inf_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.mtc2_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.delta_mtc_entry = tk.Entry(
            frame3, width=7, background='gray44', font=('times new roman', 10, 'bold'), fg='pale turquoise')

        # Layout
        self.d_moins50_sup_lbl.grid(row=1, column=3, pady=3)
        self.d_moins50_inf_lbl.grid(row=3, column=3, pady=3)
        self.d_moins50_lbl.grid(row=2, column=3, pady=3)
        self.draft_lbl.grid(row=0, column=4, pady=3)
        self.mtc2_lbl.grid(row=0, column=5, pady=3)
        self.delta_mtc_lbl.grid(row=5, column=1, padx=1, pady=10)

        self.d_moins50_sup_entry.grid(row=1, column=4, pady=3)
        self.d_moins50_inf_entry.grid(row=3, column=4, pady=3)
        self.d_moins50_entry.grid(row=2, column=4, pady=3)
        self.mtc_moins50_sup_entry.grid(row=1, column=5, pady=3)
        self.mtc_moins50_inf_entry.grid(row=3, column=5, pady=3)
        self.mtc2_entry.grid(row=2, column=5, pady=3)
        self.delta_mtc_entry.grid(row=5, column=2, pady=10)
        # Create the delta MTC button
        self.delta_MTC_button = tk.Button(
            frame3, text="Delta",
            foreground='snow',
            bg='black',
            width=8,
            command=self.delta_mtc)
        self.delta_MTC_button.grid(row=5, column=0, pady=13)

        self.mtc1_entry.configure(state=DISABLED)
        self.mtc2_entry.configure(state=DISABLED)
        self.delta_mtc_entry.configure(state=DISABLED)
        ################### Displacement ########

        self.first_trim_corr_lbl = tk.Label(frame3, text="First Trim Cor:", foreground='gold', anchor='e',
                                            background='gray12')
        self.second_trim_corr_lbl = tk.Label(frame3, text="Second Trim Cor:", foreground='gold', anchor='e',
                                             background='gray12')
        self.dis_cor_trim_lbl = tk.Label(frame3, text="Dis corr trim:", foreground='gold', anchor='e',
                                         background='gray12')
        self.density_table_lbl = tk.Label(frame3, text="Density Table:", foreground='gold', anchor='e',
                                          background='gray12')
        self.density_dock_lbl = tk.Label(frame3, text="Density Dock:", foreground='gold', anchor='e',
                                         background='gray12')
        self.dis_cor_density_lbl = tk.Label(frame3, text="Dis corr dsty :", foreground='gold', anchor='e',
                                            background='gray12')
        self.ballast_qty_lbl = tk.Label(
            frame3, text="Ballast:", foreground='gold', anchor='e', background='gray12')
        self.fuel_qty_lbl = tk.Label(
            frame3, text="Fuel:", foreground='gold', anchor='e', background='gray12')
        self.go_qty_lbl = tk.Label(
            frame3, text="GO:", foreground='gold', anchor='e', background='gray12')
        self.lub_qty_lbl = tk.Label(
            frame3, text="LO:", foreground='gold', anchor='e', background='gray12')
        self.slops_qty_lbl = tk.Label(
            frame3, text="Slops:", foreground='gold', anchor='e', background='gray12')
        self.others_qty_lbl = tk.Label(
            frame3, text="Other:", foreground='gold', anchor='e', background='gray12')

        self.correct_displacement_lbl = tk.Label(frame3, text='Displ Corrected:',
                                                 foreground='gold', anchor='e', background='gray12')
        self.total_deductibles_lbl = tk.Label(frame3, text='Deduc:',
                                              foreground='gold', anchor='e', background='gray12')
        self.net_displacement_lbl = tk.Label(frame3, text='Disp:',
                                             foreground='gold', anchor='e', background='gray12')
        self.light_ship_lbl = tk.Label(frame3, text='LightShip :',
                                       foreground='gold', anchor='e', background='gray12')
        self.constante_lbl = tk.Label(frame3, text='Car&cos:',
                                      foreground='gold', anchor='e', background='gray12')

        self.first_trim_corr_entry = tk.Entry(frame3, width=8, background='gray44',
                                              font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.second_trim_corr_entry = tk.Entry(frame3, width=8, background='gray44',
                                               font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.dis_cor_trim_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                           fg='pale turquoise')
        self.density_table_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                            fg='pale turquoise')
        self.density_dock_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                           fg='pale turquoise')
        self.dis_cor_density_entry = tk.Entry(frame3, width=8, background='gray44',
                                              font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.ballast_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                          fg='pale turquoise')
        self.fuel_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                       fg='pale turquoise')
        self.go_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                     fg='pale turquoise')
        self.lub_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                      fg='pale turquoise')
        self.slops_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                        fg='pale turquoise')
        self.others_qty_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                         fg='pale turquoise')

        self.correct_displacement_entry = tk.Entry(frame3, width=8, background='gray44',
                                                   font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.total_deductibles_entry = tk.Entry(frame3, width=8, background='gray44',
                                                font=('times new roman', 10, 'bold'), fg='pale turquoise')
        self.net_disp = tk.IntVar()
        self.net_displacement_entry = tk.Entry(frame3, width=8, background='gray44',
                                               font=('times new roman', 10, 'bold'), fg='pale turquoise',
                                               textvariable=self.net_disp)
        self.light_ship_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                         fg='pale turquoise')
        self.constante_entry = tk.Entry(frame3, width=8, background='gray44', font=('times new roman', 10, 'bold'),
                                        fg='pale turquoise')

        self.first_trim_corr_lbl.grid(row=10, column=0, padx=2, pady=8)
        self.second_trim_corr_lbl.grid(row=11, column=0, padx=2, pady=5)
        self.dis_cor_trim_lbl.grid(row=12, column=0, padx=2, pady=5)
        self.density_table_lbl.grid(row=13, column=0, padx=2, pady=7)
        self.density_dock_lbl.grid(row=14, column=0, padx=2, pady=5)
        self.dis_cor_density_lbl.grid(row=15, column=0, padx=2, pady=8)
        self.ballast_qty_lbl.grid(row=10, column=2, padx=2, pady=7)
        self.fuel_qty_lbl.grid(row=11, column=2, padx=2, pady=7)
        self.go_qty_lbl.grid(row=12, column=2, padx=2, pady=7)
        self.lub_qty_lbl.grid(row=13, column=2, padx=2, pady=7)
        self.slops_qty_lbl.grid(row=14, column=2, padx=2, pady=7)
        self.others_qty_lbl.grid(row=15, column=2, padx=2, pady=7)

        # self.correct_displacement_lbl.grid(row=10, column=4, padx=2, pady=8)
        self.total_deductibles_lbl.grid(row=11, column=4, pady=8)
        self.net_displacement_lbl.grid(row=12, column=4, pady=8)
        self.light_ship_lbl.grid(row=13, column=4, pady=8)
        self.constante_lbl.grid(row=14, column=4, pady=8)
        self.constante_lbl.config(text=f'{self.radio_var.get()}')

        self.first_trim_corr_entry.grid(row=10, column=1, padx=2, pady=8)
        self.second_trim_corr_entry.grid(row=11, column=1, padx=2, pady=5)
        self.dis_cor_trim_entry.grid(row=12, column=1, padx=2, pady=5)
        self.density_table_entry.grid(row=13, column=1, padx=2, pady=7)
        self.density_dock_entry.grid(row=14, column=1, padx=2, pady=5)
        self.dis_cor_density_entry.grid(row=15, column=1, padx=2, pady=8)
        self.ballast_qty_entry.grid(row=10, column=3, pady=7)
        self.fuel_qty_entry.grid(row=11, column=3, pady=7)
        self.go_qty_entry.grid(row=12, column=3, pady=7)
        self.lub_qty_entry.grid(row=13, column=3, pady=7)
        self.slops_qty_entry.grid(row=14, column=3, pady=7)
        self.others_qty_entry.grid(row=15, column=3, pady=7)

        # self.correct_displacement_entry.grid(row=10, column=5, padx=2, pady=8)
        self.total_deductibles_entry.grid(row=11, column=5, pady=8)
        self.net_displacement_entry.grid(row=12, column=5, pady=8)
        self.light_ship_entry.grid(row=13, column=5, pady=8)
        self.constante_entry.grid(row=14, column=5, pady=8)

        # buttons_frame
        self.btn_frame = tk.LabelFrame(frame3,
                                       font=('times new roman', 12, 'bold'), background='gray12', fg='gold',
                                       text='Command', bd=6, relief='groove')
        self.btn_frame.grid(row=18, column=0, columnspan=6, pady=12)

        self.trim_corr_btn = tk.Button(self.btn_frame, text="TC",
                                       foreground='snow',
                                       bg='black',
                                       width=8,
                                       command=self.trim_correction)
        self.trim_corr_btn.grid(row=0, column=0, padx=5, pady=6)

        self.density_corr_btn = tk.Button(self.btn_frame, text="DC",
                                          foreground='snow',
                                          bg='black',
                                          width=8,
                                          command=self.density_correction)
        self.density_corr_btn.grid(row=0, column=1, padx=5, pady=6)
        self.total_deductibles_btn = tk.Button(self.btn_frame, text="Deduc",
                                               foreground='snow',
                                               bg='black',
                                               width=8,
                                               command=self.total_deductibles)
        self.total_deductibles_btn.grid(row=0, column=2, padx=5, pady=6)

        self.net_displacement_btn = tk.Button(self.btn_frame, text="Net Disp",
                                              foreground='snow',
                                              bg='black',
                                              width=8,
                                              command=self.net_displacement)
        self.net_displacement_btn.grid(row=0, column=3, padx=5, pady=6)

        self.clear_btn = tk.Button(self.btn_frame, text="Clear",
                                   foreground='snow',
                                   bg='black',
                                   width=8,
                                   command=self.clear)
        self.clear_btn.grid(row=0, column=4, padx=5, pady=6)
        self.email_btn = tk.Button(self.btn_frame, text="Email",
                                   foreground='snow',
                                   bg='black',
                                   width=8,
                                   command=self.email)
        self.email_btn.grid(row=1, column=0, padx=5, pady=6)
        self.update_btn = tk.Button(self.btn_frame, text="Update",
                                    foreground='snow',
                                    bg='black',
                                    width=8,
                                    command=self.update)
        self.update_btn.grid(row=1, column=2, padx=5, pady=6)
        btn = tk.Button(self.btn_frame, text='Next', foreground='snow',
                        bg='black',
                        width=8, command=lambda: controller.show_frame(ThirdPage))
        btn.grid(row=1, column=3)
        btn = tk.Button(self.btn_frame, text='Back', foreground='snow',
                        bg='black',
                        width=8, command=lambda: controller.show_frame(FirstPage))
        btn.grid(row=1, column=4)

        self.dis_cor_trim_entry.configure(state=DISABLED)
        self.first_trim_corr_entry.configure(state=DISABLED)
        self.second_trim_corr_entry.configure(state=DISABLED)
        self.dis_cor_density_entry.configure(state=DISABLED)
        self.total_deductibles_entry.configure(state=DISABLED)
        self.net_displacement_entry.configure(state=DISABLED)
        self.constante_entry.configure(state=DISABLED)

        # frame4
        frame4 = tk.LabelFrame(self, text='TextArea', bg='gray12',
                               fg="gold",
                               font=('times new roman', 12, 'bold'), bd=6, relief='groove')
        frame4.pack(side='left', fill='both')

        self.textarea_lbl = tk.Label(
            frame4, text="Initial Draft Survey",
            bd=6, relief='groove',
            font=('times new roman', 12, 'bold'),
            anchor='center',
            background='gray12', fg='gold')

        self.textarea_lbl.pack(fill='x')

        # Scrollbar
        self.scrollbar = tk.Scrollbar(frame4, orient='vertical')
        self.scrollbar.pack(side='right', fill='y')

        self.textarea = tk.Text(frame4,
                                height=60, width=37,
                                yscrollcommand=Scrollbar.set)
        self.textarea.pack()
        self.scrollbar.config(command=self.textarea.yview)

        ########################### L O G I C S ####################################

    # hdbzcfxmkdqhpoqh # pour agar22thoul@gmail.com like sender
    '''def update(self, neto):
        print('net displ :', self.net_displacement_entry.get())'''

    def email(self):
        def send_gmail():
            try:
                ob = smtplib.SMTP('smtp.gmail.com', 587)
                ob.starttls()
                ob.login(sender_entry.get(), receiver_entry.get())
                sender_address = sender_entry.get()
                message = email_textarea.get(1.0, tk.END)
                receiver_address = receiver_entry.get()
                ob.sendmail(sender_address, receiver_address, message)
                ob.quit()
                messagebox.showinfo(
                    'Success', 'Your message was successfully sent')
            except:
                messagebox.showerror('Error', 'May be the password is wrong or something else,\
                 untel now i dont know what is it')

        if self.textarea.get(1.0, tk.END) == '\n':
            messagebox.showerror(
                'Error', 'There is no data in the textarea to send')
        else:
            root1 = tk.Toplevel()
            root1.title('Send Gmail')
            root1.config(bg='gray13')
            root1.resizable(0, 0)

            # Sender zone
            sender_frm = tk.LabelFrame(root1,
                                       text='Sender',
                                       font=('arial', 14, 'bold'),
                                       bd=6, bg='gray13', fg='gold')
            sender_frm.grid(row=0, column=0, padx=40, pady=20)
            sender_lbl = tk.Label(sender_frm,
                                  text="Sender's Email:",
                                  font=('arial', 13, 'bold'),
                                  bg='gray13', fg='white')
            sender_lbl.grid(row=0, column=0, padx=10, pady=8)
            sender_entry = tk.Entry(sender_frm, width=23, bd=2, relief='ridge',
                                    font=('arial', 12, 'bold'),
                                    bg='turquoise', fg='tomato')
            sender_entry.grid(row=0, column=1, padx=10, pady=8)
            password_lbl = tk.Label(sender_frm,
                                    text="Password:",
                                    font=('arial', 13, 'bold'),
                                    bg='gray13', fg='white')
            password_lbl.grid(row=1, column=0, padx=10, pady=8)
            password_entry = tk.Entry(sender_frm,
                                      width=23, bd=2, relief='ridge',
                                      font=('arial', 12, 'bold'),
                                      bg='turquoise', fg='tomato', show='*')
            password_entry.grid(row=1, column=1, padx=10, pady=8)
            # Receiver zone
            receiver_frm = tk.LabelFrame(root1,
                                         text='Receiver',
                                         font=('arial', 14, 'bold'),
                                         bd=6, bg='gray13', fg='gold')
            receiver_frm.grid(row=1, column=0, padx=40, pady=20)

            receiver_lbl = tk.Label(receiver_frm,
                                    text="Email address:",
                                    font=('arial', 13, 'bold'),
                                    bg='gray13', fg='white')
            receiver_lbl.grid(row=0, column=0, padx=10, pady=8)
            receiver_entry = tk.Entry(receiver_frm,
                                      width=23, bd=2, relief='ridge',
                                      font=('arial', 12, 'bold'),
                                      bg='turquoise', fg='tomato')
            receiver_entry.grid(row=0, column=1, padx=10, pady=8)
            message_lbl = tk.Label(receiver_frm,
                                   text="Message:",
                                   font=('arial', 12, 'bold'),
                                   bg='gray13', fg='white')
            message_lbl.grid(row=1, column=0, padx=10, pady=8)
            # textArea
            email_textarea = tk.Text(receiver_frm,
                                     font=('arial', 12, 'bold'),
                                     bd=2, width=38, height=15,
                                     relief='sunken')
            email_textarea.grid(row=2, column=0, columnspan=2)
            email_textarea.delete(1.0, tk.END)
            email_textarea.insert(tk.END, self.textarea.get(1.0, tk.END))

            # Sending Button
            gmail_btn = tk.Button(root1, width=15, fg='gold',
                                  text='Send', bg="gray16",
                                  font=('arial', 12, 'bold'),
                                  command=send_gmail)

            gmail_btn.grid(row=2, column=0, pady=20)

            root1.mainloop()

    def print(self):
        if self.textarea.get(1.0, tk.END) == '\n':
            messagebox.showerror(
                'Error', 'There is no data in the textarea to print')
        else:
            file = tempfile.mktemp('.txt')
            open(file, 'w').write(self.textarea.get(1.0, tk.END))
            os.startfile(file, 'print')

    def search_data(self):
        for i in os.listdir('Output/'):
            if i.split('.')[0] == self.draft_number_entry.get():
                f = open(f'Output/{i}', 'r')
                self.textarea.delete(1.0, tk.END)
                for data in f:
                    self.textarea.insert(tk.END, data)
                f.close()
                break
        else:
            messagebox.showerror('Error', 'Invalid Draft Number')

    def choice(self):

        if self.radio_var.get() == 'load':  # 'loading' radio button selected
            self.constante_lbl.config(text='Const')
            self.net_displacement_lbl.config(text='Net disp')
            self.light_ship_lbl.config(text='Lightship')
            self.net_displacement_btn.config(text='Const')
        elif self.radio_var.get() == 'discharge':  # 'discharging' radio button selected
            self.constante_lbl.config(text='Cargo + Const')
            self.net_displacement_lbl.config(text='Load disp')
            self.light_ship_lbl.config(text='Lightship')
            self.net_displacement_btn.config(text='Load Disp')

    def clear(self):

        self.lbm_entry.configure(state=NORMAL)
        self.obs_trim_entry.configure(state=NORMAL)
        self.corrected_for_entry.configure(state=NORMAL)
        self.corrected_aft_entry.configure(state=NORMAL)
        self.corrected_mid_entry.configure(state=NORMAL)
        self.mean_for_aft_entry.configure(state=NORMAL)
        self.mean_of_mean_entry.configure(state=NORMAL)
        self.quarter_mean_entry.configure(state=NORMAL)
        self.init_draft_entry.configure(state=NORMAL)
        self.init_tpc_entry.configure(state=NORMAL)
        self.init_displacement_entry.configure(state=NORMAL)
        self.init_lcf_entry.configure(state=NORMAL)
        self.mtc1_entry.configure(state=NORMAL)
        self.mtc2_entry.configure(state=NORMAL)
        self.delta_mtc_entry.configure(state=NORMAL)
        self.first_trim_corr_entry.configure(state=NORMAL)
        self.second_trim_corr_entry.configure(state=NORMAL)
        self.dis_cor_trim_entry.configure(state=NORMAL)
        self.dis_cor_density_entry.configure(state=NORMAL)
        self.total_deductibles_entry.configure(state=NORMAL)
        self.net_displacement_entry.configure(state=NORMAL)
        self.constante_entry.configure(state=NORMAL)

        self.vessel_entry.delete(0, tk.END)
        self.flag_entry.delete(0, tk.END)
        self.registry_entry.delete(0, tk.END)
        self.imo_entry.delete(0, tk.END)
        self.cargo_entry.delete(0, tk.END)
        self.client_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.load_port_entry.delete(0, tk.END)
        self.disch_port_entry.delete(0, tk.END)
        self.arrival_time.delete(0, tk.END)
        self.birthing_time.delete(0, tk.END)
        self.initialds_time.delete(0, tk.END)
        self.cal1.delete(0, tk.END)
        self.cal2.delete(0, tk.END)
        self.cal3.delete(0, tk.END)

        self.lbp_entry.delete(0, tk.END)
        self.draft_for_port_entry.delete(0, tk.END)
        self.draft_for_star_entry.delete(0, tk.END)
        self.draft_aft_port_entry.delete(0, tk.END)
        self.draft_aft_star_entry.delete(0, tk.END)
        self.draft_mid_port_entry.delete(0, tk.END)
        self.draft_mid_star_entry.delete(0, tk.END)
        self.lbm_entry.delete(0, tk.END)
        self.obs_trim_entry.delete(0, tk.END)
        self.distance_from_for_pp_entry.delete(0, tk.END)
        self.distance_from_aft_pp_entry.delete(0, tk.END)
        self.distance_from_mid_pp_entry.delete(0, tk.END)
        self.corrected_for_entry.delete(0, tk.END)
        self.corrected_aft_entry.delete(0, tk.END)
        self.corrected_mid_entry.delete(0, tk.END)
        self.mean_for_aft_entry.delete(0, tk.END)
        self.mean_of_mean_entry.delete(0, tk.END)
        self.quarter_mean_entry.delete(0, tk.END)
        self.position_from_for_pp_combobox.delete(0, tk.END)
        self.position_from_aft_pp_combobox.delete(0, tk.END)
        self.position_from_mid_pp_combobox.delete(0, tk.END)

        self.draft_sup_entry.delete(0, tk.END)
        self.init_draft_entry.delete(0, tk.END)
        self.draft_inf_entry.delete(0, tk.END)
        self.displacement_sup_entry.delete(0, tk.END)
        self.init_displacement_entry.delete(0, tk.END)
        self.displacement_inf_entry.delete(0, tk.END)
        self.tpc_sup_entry.delete(0, tk.END)
        self.init_tpc_entry.delete(0, tk.END)
        self.tpc_inf_entry.delete(0, tk.END)
        self.lcf_sup_entry.delete(0, tk.END)
        self.init_lcf_entry.delete(0, tk.END)
        self.lcf_inf_entry.delete(0, tk.END)

        self.d_plus50_sup_entry.delete(0, tk.END)
        self.d_plus50_inf_entry.delete(0, tk.END)
        self.d_plus50_entry.delete(0, tk.END)
        self.mtc_plus50_sup_entry.delete(0, tk.END)
        self.mtc_plus50_inf_entry.delete(0, tk.END)
        self.mtc1_entry.delete(0, tk.END)
        self.d_moins50_sup_entry.delete(0, tk.END)
        self.d_moins50_inf_entry.delete(0, tk.END)
        self.d_moins50_entry.delete(0, tk.END)
        self.mtc_moins50_sup_entry.delete(0, tk.END)
        self.mtc_moins50_inf_entry.delete(0, tk.END)
        self.mtc2_entry.delete(0, tk.END)
        self.delta_mtc_entry.delete(0, tk.END)

        self.first_trim_corr_entry.delete(0, tk.END)
        self.second_trim_corr_entry.delete(0, tk.END)
        self.dis_cor_trim_entry.delete(0, tk.END)
        self.density_table_entry.delete(0, tk.END)
        self.density_dock_entry.delete(0, tk.END)
        self.dis_cor_density_entry.delete(0, tk.END)
        self.ballast_qty_entry.delete(0, tk.END)
        self.fuel_qty_entry.delete(0, tk.END)
        self.go_qty_entry.delete(0, tk.END)
        self.lub_qty_entry.delete(0, tk.END)
        self.slops_qty_entry.delete(0, tk.END)
        self.others_qty_entry.delete(0, tk.END)
        self.net_displacement_entry.delete(0, tk.END)
        self.light_ship_entry.delete(0, tk.END)
        self.correct_displacement_entry.delete(0, tk.END)
        self.total_deductibles_entry.delete(0, tk.END)
        self.constante_entry.delete(0, tk.END)

        self.draft_number_entry.delete(0, tk.END)
        self.textarea.delete(1.0, tk.END)

        self.lbm_entry.configure(state=DISABLED)
        self.obs_trim_entry.configure(state=DISABLED)
        self.corrected_for_entry.configure(state=DISABLED)
        self.corrected_aft_entry.configure(state=DISABLED)
        self.corrected_mid_entry.configure(state=DISABLED)
        self.mean_for_aft_entry.configure(state=DISABLED)
        self.mean_of_mean_entry.configure(state=DISABLED)
        self.quarter_mean_entry.configure(state=DISABLED)
        self.init_draft_entry.configure(state=DISABLED)
        self.init_tpc_entry.configure(state=DISABLED)
        self.init_displacement_entry.configure(state=DISABLED)
        self.init_lcf_entry.configure(state=DISABLED)
        self.mtc1_entry.configure(state=DISABLED)
        self.mtc2_entry.configure(state=DISABLED)
        self.delta_mtc_entry.configure(state=DISABLED)
        self.first_trim_corr_entry.configure(state=DISABLED)
        self.second_trim_corr_entry.configure(state=DISABLED)
        self.dis_cor_trim_entry.configure(state=DISABLED)
        self.dis_cor_density_entry.configure(state=DISABLED)
        self.total_deductibles_entry.configure(state=DISABLED)
        self.net_displacement_entry.configure(state=DISABLED)
        self.constante_entry.configure(state=DISABLED)

        self.vessel_entry.focus()

    def net_displacement(self):

        self.net_displacement_entry.configure(state=NORMAL)
        # self.load_displacement_entry.configure(state=NORMAL)
        self.constante_entry.configure(state=NORMAL)

        total_deductibles = self.total_deductibles_entry.get()
        corrected_displacement_for_density = self.dis_cor_density_entry.get()
        net_displacement = ''
        light_ship = self.light_ship_entry.get()
        constante = ''

        if total_deductibles == '' or corrected_displacement_for_density == '' or light_ship == '':
            messagebox.showerror('Error', 'The total deductibles the corrected displacement\
             for density or the light ship is missed')
        else:
            total_deductibles = float(total_deductibles)
            corrected_displacement_for_density = float(
                corrected_displacement_for_density)
            light_ship = float(light_ship)
            net_displacement = round(
                corrected_displacement_for_density - total_deductibles, 3)
            constante = round(net_displacement - light_ship)

        self.net_displacement_entry.delete(0, tk.END)
        self.constante_entry.delete(0, tk.END)
        # self.load_displacement_entry.delete(0, tk.END)
        self.net_displacement_entry.insert(tk.END, f'{net_displacement}')
        self.constante_entry.insert(tk.END, f'{constante}')
        # self.load_displacement_entry.insert(tk.END, f'{net_displacement}')
        self.net_displacement_entry.configure(state=DISABLED)
        self.constante_entry.configure(state=DISABLED)

        messagebox.showinfo(
            'Success', "we get the net displacement & the calculated constante ")

    def total_deductibles(self):
        self.total_deductibles_entry.configure(state=NORMAL)
        ballast = self.ballast_qty_entry.get()
        fuel = self.fuel_qty_entry.get()
        gas_oil = self.go_qty_entry.get()
        lub_oil = self.lub_qty_entry.get()
        slops = self.slops_qty_entry.get()
        others = self.others_qty_entry.get()
        total_deductibles = ''

        if ballast == '' or fuel == '' or gas_oil == '' or lub_oil == '' or \
                slops == '' or others == '':
            messagebox.showerror(
                'Error', 'Please some deductibles input are empty')
        else:
            ballast = float(ballast)
            fuel = float(fuel)
            gas_oil = float(gas_oil)
            lub_oil = float(lub_oil)
            slops = float(slops)
            others = float(others)

        total_deductibles = round(
            ballast + fuel + gas_oil + lub_oil + slops + others, 3)

        self.total_deductibles_entry.delete(0, tk.END)
        self.total_deductibles_entry.insert(tk.END, f'{total_deductibles}')
        self.total_deductibles_entry.configure(state=DISABLED)
        messagebox.showinfo('Success', 'we get the total deductibles ')

    def density_correction(self):
        self.dis_cor_density_entry.configure(state=NORMAL)
        table_density = self.density_table_entry.get()
        dock_density = self.density_dock_entry.get()
        corrected_displacement_for_trim = self.dis_cor_trim_entry.get()
        corrected_displacement_for_density = ''

        if table_density == '' or dock_density == '' or \
                corrected_displacement_for_trim == '':
            messagebox.showerror(
                'Error', 'Please insert the table and the observed density')
        else:
            table_density = float(table_density)
            dock_density = float(dock_density)
            corrected_displacement_for_trim = float(
                corrected_displacement_for_trim)
            corrected_displacement_for_density = round(
                (corrected_displacement_for_trim * dock_density) / table_density,
                3)
        self.dis_cor_density_entry.delete(0, tk.END)
        self.dis_cor_density_entry.insert(
            tk.END, f'{corrected_displacement_for_density}')
        messagebox.showinfo(
            'Success', 'Great now you corrected the displacement for the density')
        self.dis_cor_density_entry.configure(state=DISABLED)

    def trim_correction(self):
        self.dis_cor_trim_entry.configure(state=NORMAL)
        self.first_trim_corr_entry.configure(state=NORMAL)
        self.second_trim_corr_entry.configure(state=NORMAL)

        draft_for_corr = float(self.corrected_for_entry.get())
        draft_aft_corr = float(self.corrected_aft_entry.get())
        trim_corrected = ''
        tpc = float(self.init_tpc_entry.get())
        lcf = float(self.init_lcf_entry.get())
        lbp = float(self.lbp_entry.get())
        delta_mtc = float(self.delta_mtc_entry.get())
        displacement = float(self.init_displacement_entry.get())

        if self.corrected_for_entry.get() == '' or self.corrected_aft_entry.get() == '' or \
                self.init_tpc_entry.get() == '' or self.init_lcf_entry.get() == '' or \
                self.lbp_entry.get() == '' or self.delta_mtc_entry.get() == '':
            messagebox.showerror(
                'Error', 'Please fill all the fields required for the 1st Trim Correction')
        else:
            trim_corrected = draft_aft_corr - draft_for_corr
            first_trim_correction = round(
                (trim_corrected * 100 * tpc * lcf) / lbp, 2)
            second_trim_correction = round(
                (trim_corrected * trim_corrected * 50 * delta_mtc) / lbp, 2)
            corrected_displacement_for_trim = round(
                displacement + first_trim_correction + second_trim_correction, 2)

            self.dis_cor_trim_entry.delete(0, tk.END)
            self.first_trim_corr_entry.delete(0, tk.END)
            self.second_trim_corr_entry.delete(0, tk.END)

            self.dis_cor_trim_entry.insert(
                tk.END, f'{corrected_displacement_for_trim}')
            self.first_trim_corr_entry.insert(
                tk.END, f'{first_trim_correction} ')
            self.second_trim_corr_entry.insert(
                tk.END, f'{second_trim_correction}')
            messagebox.showinfo(
                'Success', 'Great you have just correct the displacement for the trim')

        self.dis_cor_trim_entry.configure(state=DISABLED)
        self.first_trim_corr_entry.configure(state=DISABLED)
        self.second_trim_corr_entry.configure(state=DISABLED)

    def save_data(self):
        if self.vessel_entry.get() == '' or self.flag_entry.get() == '' or \
                self.registry_entry.get() == '' or self.imo_entry.get() == '' or \
                self.cargo_entry.get() == '' or self.client_entry.get() == '' or \
                self.quantity_entry.get() == '' or self.load_port_entry.get() == '' or \
                self.disch_port_entry.get() == '' or self.cal1.get() == '' or self.cal2.get() == '' or \
                self.cal3.get() == '' or self.arrival_time.get() == '' or self.birthing_time.get() == '' or \
                self.initialds_time.get() == '':
            messagebox.showerror(
                'Error', "Vessel's Information are all required")
        elif self.lbp_entry.get() == '' or self.draft_for_star_entry.get() == '' or \
                self.draft_for_port_entry.get() == '' or self.position_from_aft_pp_combobox.get() == '' or \
                self.draft_aft_port_entry.get() == '' or self.draft_aft_star_entry.get() == '' or \
                self.draft_mid_port_entry.get() == '' or self.draft_mid_star_entry.get() == '' or \
                self.distance_from_for_pp_entry.get() == '' or self.distance_from_aft_pp_entry.get() == '' or \
                self.distance_from_mid_pp_entry.get() == '' or self.position_from_for_pp_combobox.get() == '' or \
                self.position_from_mid_pp_combobox.get() == '':
            messagebox.showerror('Error', "Draft entries are all required")
        elif self.obs_trim_entry.get() == '' or self.lbp_entry.get() == '' or \
                self.corrected_for_entry.get() == '' or self.corrected_aft_entry.get() == '' or \
                self.corrected_mid_entry.get() == '' or self.mean_for_aft_entry.get() == '' or \
                self.mean_of_mean_entry.get() == '' or self.quarter_mean_entry.get() == '':
            messagebox.showerror('Error', "Correct the Observed Draft first")
        else:
            self.textarea.delete(1.0, tk.END)

            self.textarea.insert(tk.END, '***Initial Draft Survey ***\n')
            self.textarea.insert(
                tk.END, f'\nVessel: {self.vessel_entry.get()}\tSGS_{self.draft_number_entry.get()}\n')
            self.textarea.insert(tk.END, f'Nation: {self.flag_entry.get()}\n')
            self.textarea.insert(
                tk.END, f'Reg.Port: {self.registry_entry.get()}\n')
            self.textarea.insert(tk.END, f'IMO: {self.imo_entry.get()}\n')
            self.textarea.insert(tk.END, f'Cargo: {self.cargo_entry.get()}\n')
            self.textarea.insert(
                tk.END, f'Client: {self.client_entry.get()}\n')
            self.textarea.insert(
                tk.END, f'Quantity: {self.quantity_entry.get()} Mt\n')
            self.textarea.insert(
                tk.END, f'Load_port: {self.load_port_entry.get()}\n')
            self.textarea.insert(
                tk.END, f'Dis_port: {self.disch_port_entry.get()}\n')
            self.textarea.insert(
                tk.END, f'Arrival: {self.cal1.get()}\t at : {self.arrival_time.get()}\n')
            self.textarea.insert(
                tk.END, f'Birthing: {self.cal2.get()}\t at : {self.birthing_time.get()}\n')
            self.textarea.insert(
                tk.END, f'Survey: {self.cal3.get()}\t at : {self.initialds_time.get()}\n')
            self.textarea.insert(tk.END, '\n===========================\n')
            self.textarea.insert(tk.END, 'Observed Draft\n')
            self.textarea.insert(tk.END,
                                 f'Dfp: {self.draft_for_port_entry.get()} m\t Dfs: {self.draft_for_star_entry.get()}m\n')
            self.textarea.insert(tk.END,
                                 f'Dmp: {self.draft_mid_port_entry.get()} m\t Dfs: {self.draft_mid_star_entry.get()}m\n')
            self.textarea.insert(tk.END,
                                 f'Dap: {self.draft_aft_port_entry.get()} m\t Dfs: {self.draft_aft_star_entry.get()}m\n')
            self.textarea.insert(tk.END, '\n===========================\n')
            self.textarea.insert(tk.END, 'Corrected Draft:\n')
            self.textarea.insert(
                tk.END, f'Trim Ob: {self.obs_trim_entry.get()}m\t Lbm:{self.lbm_entry.get()}m\n')
            self.textarea.insert(tk.END,
                                 f'Dfc: {self.corrected_for_entry.get()} m\t Dac: {self.corrected_aft_entry.get()}m\n')
            self.textarea.insert(
                tk.END, f'Dmc: {self.corrected_mid_entry.get()} m\n')
            self.textarea.insert(
                tk.END, f'Dfa: {self.mean_for_aft_entry.get()} m\n')
            self.textarea.insert(
                tk.END, f'Mom: {self.mean_of_mean_entry.get()} m\n')
            self.textarea.insert(
                tk.END, f'QM: {self.quarter_mean_entry.get()} m\n')
            self.textarea.insert(tk.END, '\n===========================\n')
            self.textarea.insert(tk.END, 'Displacement Corrections:\n')
            self.textarea.insert(
                tk.END, f'Displacement: {self.init_displacement_entry.get()} mt\n')
            self.textarea.insert(
                tk.END, f'Dis Corrected for trim: {self.dis_cor_trim_entry.get()} mt\n')
            self.textarea.insert(
                tk.END, f'Dis Corrected for density: {self.dis_cor_density_entry.get()} mt\n')
            self.textarea.insert(
                tk.END, f'Total deductibles: {self.total_deductibles_entry.get()} mt\n')
            self.textarea.insert(
                tk.END, f'Net Displacement: {self.net_displacement_entry.get()} mt\n')
            self.textarea.insert(
                tk.END, f'Cargo + const: {self.constante_entry.get()} mt\n')

            self.draft_number_entry.insert(tk.END, f'SGS_{draft_number}')
            self.save()

    def save(self):
        global draft_number
        result = messagebox.showinfo(
            'Confirm', 'Do you want to save the data input?')
        if result:
            draft_content = self.textarea.get(1.0, tk.END)
            file = open(f'Output/{draft_number}.txt', 'w')
            file.write(draft_content)
            file.close()
            messagebox.showinfo(
                'Success', f'The initial draft survey number:f{draft_number} is saved successfully')

    def delta_mtc(self):
        # Mtc 1
        self.mtc1_entry.configure(state=NORMAL)
        self.mtc2_entry.configure(state=NORMAL)
        self.delta_mtc_entry.configure(state=NORMAL)

        d_plus50_sup = self.d_plus50_sup_entry.get()
        d_plus50_inf = self.d_plus50_inf_entry.get()
        d_plus50 = self.d_plus50_entry.get()

        mtc_plus50_sup = self.mtc_plus50_sup_entry.get()
        mtc_plus50_inf = self.mtc_plus50_inf_entry.get()

        if d_plus50_sup and d_plus50_inf and d_plus50 and mtc_plus50_sup and mtc_plus50_inf:
            try:
                d_plus50_sup = float(d_plus50_sup)
                d_plus50_inf = float(d_plus50_inf)
                d_plus50 = float(d_plus50)
                mtc_plus50_sup = float(mtc_plus50_sup)
                mtc_plus50_inf = float(mtc_plus50_inf)

                mtc1 = round((((mtc_plus50_sup - mtc_plus50_inf) / (d_plus50_sup - d_plus50_inf)) *
                              (d_plus50_sup - d_plus50)) + mtc_plus50_inf, 2)

                self.mtc1_entry.delete(0, tk.END)
                self.mtc1_entry.insert(tk.END, str(mtc1))
            except ValueError:
                self.mtc1_entry.delete(0, tk.END)
                self.mtc1_entry.insert(tk.END, "Invalid value")
        else:
            self.mtc1_entry.delete(0, tk.END)
            self.mtc1_entry.insert(tk.END, "Missing values")

        # Mtc 2

        d_moins50_sup = self.d_moins50_sup_entry.get()
        d_moins50_inf = self.d_moins50_inf_entry.get()
        d_moins50 = self.d_moins50_entry.get()

        mtc_moins50_sup = self.mtc_moins50_sup_entry.get()
        mtc_moins50_inf = self.mtc_moins50_inf_entry.get()

        if d_moins50_sup and d_moins50_inf and d_moins50 and mtc_moins50_sup and mtc_moins50_inf:
            try:
                d_moins50_sup = float(d_moins50_sup)
                d_moins50_inf = float(d_moins50_inf)
                d_moins50 = float(d_moins50)
                mtc_moins50_sup = float(mtc_moins50_sup)
                mtc_moins50_inf = float(mtc_moins50_inf)

                mtc2 = round((((mtc_moins50_sup - mtc_moins50_inf) / (d_moins50_sup - d_moins50_inf)) *
                              (d_moins50_sup - d_moins50)) + mtc_moins50_inf, 2)

                self.mtc2_entry.delete(0, tk.END)
                self.mtc2_entry.insert(tk.END, str(mtc2))
            except ValueError:
                self.mtc2_entry.delete(0, tk.END)
                self.mtc2_entry.insert(tk.END, "Invalid value")
        else:
            self.mtc2_entry.delete(0, tk.END)
            self.mtc2_entry.insert(tk.END, "Missing values")

        # Delta MTC
        if isinstance(mtc1, float) and isinstance(mtc2, float):
            delta_mtc = round(mtc1 - mtc2, 2)
            self.delta_mtc_entry.delete(0, tk.END)
            self.delta_mtc_entry.insert(tk.END, str(delta_mtc))
        else:
            self.delta_mtc_entry.delete(0, tk.END)
            self.delta_mtc_entry.insert(tk.END, "Invalid values")

        self.mtc1_entry.configure(state=DISABLED)
        self.mtc2_entry.configure(state=DISABLED)
        self.delta_mtc_entry.configure(state=DISABLED)

    def validate_interpolation_input(self):
        # Validate draft_sup_entry
        draft_sup = self.draft_sup_entry.get()
        if not draft_sup or not all(char.isdigit() or char == '.' for char in draft_sup):
            return False

        # Validate draft_inf_entry
        draft_inf = self.draft_inf_entry.get()
        if not draft_inf or not all(char.isdigit() or char == '.' for char in draft_inf):
            return False

        # Validate displacement_inf_entry
        displacement_inf = self.displacement_inf_entry.get()
        if not displacement_inf or not all(char.isdigit() or char == '.' for char in displacement_inf):
            return False

        # Validate displacement_sup_entry
        displacement_sup = self.displacement_sup_entry.get()
        if not displacement_sup or not all(char.isdigit() or char == '.' for char in displacement_sup):
            return False

        # Validate tpc_sup_entry
        tpc_sup = self.tpc_sup_entry.get()
        if not tpc_sup or not all(char.isdigit() or char == '.' for char in tpc_sup):
            return False
        # Validate tpc_inf_entry
        tpc_inf = self.tpc_inf_entry.get()
        if not tpc_inf or not all(char.isdigit() or char == '.' for char in tpc_inf):
            return False

        # Validate lcf_sup_entry
        lcf_sup = self.lcf_sup_entry.get()
        if not lcf_sup or not all(char.isdigit() or char == '.' for char in lcf_sup):
            return False
        # Validate lcf_sup_entry
        lcf_inf = self.lcf_inf_entry.get()
        if not lcf_inf or not all(char.isdigit() or char == '.' for char in lcf_inf):
            return False

        return True

    def calculate_interpolation(self):
        self.quarter_mean_entry.configure(state=NORMAL)
        self.init_displacement_entry.configure(state=NORMAL)
        self.init_tpc_entry.configure(state=NORMAL)
        self.init_lcf_entry.configure(state=NORMAL)
        self.init_draft_entry.configure(state=NORMAL)

        if not self.validate_interpolation_input():
            self.text_lbl.configure(text='Invalid input')
            return

        draft_sup = float(self.draft_sup_entry.get())
        draft_inf = float(self.draft_inf_entry.get())
        init_draft = float(self.quarter_mean_entry.get())
        init_displacement = 0
        displacement_sup = float(self.displacement_sup_entry.get())
        displacement_inf = float(self.displacement_inf_entry.get())
        init_tpc = 0
        tpc_sup = float(self.tpc_sup_entry.get())
        tpc_inf = float(self.tpc_inf_entry.get())
        init_lcf = 0
        lcf_sup = float(self.lcf_sup_entry.get())
        lcf_inf = float(self.lcf_inf_entry.get())

        # Perform the interpolation calculations here
        if self.init_displacement_entry.get() == '':
            try:
                init_displacement = round((((displacement_sup - displacement_inf) / (draft_sup - draft_inf)) *
                                           (draft_sup - init_draft)) + displacement_inf, 3)
                self.init_displacement_entry.delete(0, tk.END)
                self.init_displacement_entry.insert(
                    tk.END, str(init_displacement))
            except ValueError:
                self.init_displacement_entry.delete(0, tk.END)
                self.init_displacement_entry.insert(tk.END, "Invalid value")

        if self.init_tpc_entry.get() == '':
            try:
                init_tpc = round((((tpc_sup - tpc_inf) / (draft_sup - draft_inf)) *
                                  (draft_sup - init_draft)) + tpc_inf, 3)
                self.init_tpc_entry.delete(0, tk.END)
                self.init_tpc_entry.insert(tk.END, str(init_tpc))
            except ValueError:
                self.init_tpc_entry.delete(0, tk.END)
                self.init_tpc_entry.insert(tk.END, "Invalid value")

        if self.init_lcf_entry.get() == '':
            try:
                init_lcf = round((((lcf_sup - lcf_inf) / (draft_sup - draft_inf)) *
                                  (draft_sup - init_draft)) + lcf_inf, 3)
                self.init_lcf_entry.delete(0, tk.END)
                self.init_lcf_entry.insert(tk.END, str(init_lcf))
            except ValueError:
                self.init_lcf_entry.delete(0, tk.END)
                self.init_lcf_entry.insert(tk.END, "Invalid value")

        self.quarter_mean_entry.configure(state=DISABLED)
        self.init_displacement_entry.configure(state=DISABLED)
        self.init_tpc_entry.configure(state=DISABLED)
        self.init_lcf_entry.configure(state=DISABLED)
        self.init_draft_entry.configure(state=DISABLED)

        # self.text_lbl.configure(text='Interpolation completed')

    def validate_input(self):
        # Validate LBP
        lbp = self.lbp_entry.get()
        if not lbp or not all(char.isdigit() or char == '.' for char in lbp):
            return False

        # Validate Draft Forward Port side
        draft_for_port = self.draft_for_port_entry.get()
        if not draft_for_port or not all(char.isdigit() or char == '.' for char in draft_for_port):
            return False
        # Validate Draft Forward starboard side
        draft_for_star = self.draft_for_star_entry.get()
        if not draft_for_star or not all(char.isdigit() or char == '.' for char in draft_for_star):
            return False
        # Validate Draft Aft port side
        draft_aft_port = self.draft_aft_port_entry.get()
        if not draft_aft_port or not all(char.isdigit() or char == '.' for char in draft_aft_port):
            return False
        # Validate Draft Aft starboard side
        draft_aft_star = self.draft_aft_star_entry.get()
        if not draft_aft_star or not all(char.isdigit() or char == '.' for char in draft_aft_star):
            return False

        # Validate Mid_ship Draft port side
        draft_mid_port = self.draft_mid_port_entry.get()
        if not draft_mid_port or not all(char.isdigit() or char == '.' for char in draft_mid_port):
            return False
        # Validate Mid ship Draft starboard side
        draft_mid_star = self.draft_mid_star_entry.get()
        if not draft_mid_star or not all(char.isdigit() or char == '.' for char in draft_mid_star):
            return False

        # Validate Distance from ForPP
        distance_from_for_pp = self.distance_from_for_pp_entry.get()
        if not distance_from_for_pp or not all(char.isdigit() or char == '.' for char in distance_from_for_pp):
            return False

        # Validate Distance from AftPP
        distance_from_aft_pp = self.distance_from_aft_pp_entry.get()
        if not distance_from_aft_pp or not all(char.isdigit() or char == '.' for char in distance_from_aft_pp):
            return False

        # Validate Distance from MidPP
        distance_from_mid_pp = self.distance_from_mid_pp_entry.get()
        if not distance_from_mid_pp or not all(char.isdigit() or char == '.' for char in distance_from_mid_pp):
            return False

        return True

    def calculate_values(self):
        self.obs_trim_entry.configure(state=NORMAL)
        self.lbm_entry.configure(state=NORMAL)
        self.init_draft_entry.configure(state=NORMAL)
        self.corrected_for_entry.configure(state=NORMAL)
        self.corrected_aft_entry.configure(state=NORMAL)
        self.corrected_mid_entry.configure(state=NORMAL)
        self.mean_for_aft_entry.configure(state=NORMAL)
        self.mean_of_mean_entry.configure(state=NORMAL)
        self.quarter_mean_entry.configure(state=NORMAL)
        self.init_draft_entry.configure(state=NORMAL)

        if not self.validate_input():
            self.result_lbl.configure(text="Invalid input")
            return

        self.lbp = float(self.lbp_entry.get())
        self.draft_for_port = float(self.draft_for_port_entry.get())
        self.draft_for_star = float(self.draft_for_star_entry.get())
        self.draft_aft_port = float(self.draft_aft_port_entry.get())
        self.draft_aft_star = float(self.draft_aft_star_entry.get())
        self.draft_mid_port = float(self.draft_mid_port_entry.get())
        self.draft_mid_star = float(self.draft_mid_star_entry.get())
        self.distance_from_for_pp = float(
            self.distance_from_for_pp_entry.get())
        self.distance_from_aft_pp = float(
            self.distance_from_aft_pp_entry.get())
        self.distance_from_mid_pp = float(
            self.distance_from_mid_pp_entry.get())
        self.position_from_for_pp = self.position_from_for_pp_combobox.get()
        self.position_from_aft_pp = self.position_from_aft_pp_combobox.get()
        self.position_from_mid_pp = self.position_from_mid_pp_combobox.get()

        def calculate_lbm(lbp, distance_from_for_pp, distance_from_aft_pp, position_from_for_pp,
                          position_from_aft_pp):
            lbm_dict = {
                ('A', 'A'): lbp - distance_from_aft_pp - distance_from_for_pp,
                ('A', 'F'): lbp - distance_from_aft_pp + distance_from_for_pp,
                ('F', 'A'): lbp + distance_from_aft_pp + distance_from_for_pp,
                ('F', 'F'): lbp + distance_from_for_pp - distance_from_aft_pp,
                ('A', 'N/A'): lbp - distance_from_for_pp,
                ('F', 'N/A'): lbp + distance_from_for_pp,
                ('N/A', 'A'): lbp + distance_from_aft_pp,
                ('N/A', 'F'): lbp - distance_from_aft_pp
            }
            return lbm_dict.get((position_from_for_pp, position_from_aft_pp), lbp)

        lbm = round(calculate_lbm(self.lbp,
                                  self.distance_from_for_pp,
                                  self.distance_from_aft_pp,
                                  self.position_from_for_pp,
                                  self.position_from_aft_pp), 2)

        ########################

        # Draft observed
        draft_for = (self.draft_for_star + self.draft_for_port) / 2
        draft_aft = (self.draft_aft_star + self.draft_aft_port) / 2
        draft_mid = (self.draft_mid_star + self.draft_mid_port) / 2

        # Trim observed
        trim_observed = round(draft_aft - draft_for, 2)
        # Draft corrected
        # For Draft:
        if trim_observed > 0:
            if self.position_from_for_pp == "A":
                draft_for_corrected = round(
                    draft_for - ((trim_observed * self.distance_from_for_pp) / lbm), 2)
            elif self.position_from_for_pp == "F":
                draft_for_corrected = round(
                    draft_for + ((trim_observed * self.distance_from_for_pp) / lbm), 2)
        elif trim_observed < 0:
            if self.position_from_for_pp == "A":
                draft_for_corrected = round(
                    draft_for + ((abs(trim_observed) * self.distance_from_for_pp) / lbm), 2)
            elif self.position_from_for_pp == "F":
                draft_for_corrected = round(
                    draft_for - ((abs(trim_observed) * self.distance_from_for_pp) / lbm), 2)

        elif self.position_from_for_pp == "N/A":
            draft_for_corrected = round(draft_for, 2)
        elif trim_observed == 0:
            draft_for_corrected = round(draft_for, 2)

        # Aft Draft:
        draft_aft_corrected = ''
        if trim_observed > 0:
            if self.position_from_aft_pp == "A":
                draft_aft_corrected = round(
                    draft_aft - ((trim_observed * self.distance_from_aft_pp) / lbm), 2)
            elif self.position_from_aft_pp == "F":
                draft_aft_corrected = round(
                    draft_aft + ((trim_observed * self.distance_from_aft_pp) / lbm), 2)
        elif trim_observed < 0:
            if self.position_from_aft_pp == "A":
                draft_aft_corrected = round(
                    draft_aft + ((abs(trim_observed) * self.distance_from_aft_pp) / lbm), 2)
            elif self.position_from_aft_pp == "F":
                draft_aft_corrected = round(
                    draft_aft - ((abs(trim_observed) * self.distance_from_aft_pp) / lbm), 2)
        elif self.position_from_aft_pp == "N/A":
            draft_aft_corrected = round(draft_aft, 2)
        elif trim_observed == 0:
            draft_aft_corrected = round(draft_aft, 2)
        # Mid Draft:
        draft_mid_corrected = ''
        if trim_observed > 0:
            if self.position_from_mid_pp == "A":
                draft_mid_corrected = round(draft_mid - ((trim_observed * self.distance_from_mid_pp) / lbm),
                                            2)
            elif self.position_from_mid_pp == "F":
                draft_mid_corrected = round(
                    draft_mid + ((trim_observed * self.distance_from_mid_pp) / lbm), 2)
        elif trim_observed < 0:
            if self.position_from_mid_pp == "A":
                draft_mid_corrected = round(
                    draft_mid + ((abs(trim_observed) * self.distance_from_mid_pp) / lbm), 2)
            elif self.position_from_mid_pp == "F":
                draft_mid_corrected = round(
                    draft_mid - ((abs(trim_observed) * self.distance_from_mid_pp) / lbm), 2)
        elif self.position_from_mid_pp == "N/A":
            draft_mid_corrected = round(draft_mid, 2)
        elif trim_observed == 0:
            draft_mid_corrected = round(draft_mid, 2)

        self.obs_trim_entry.delete(0, tk.END)
        self.lbm_entry.delete(0, tk.END)
        self.corrected_for_entry.delete(0, tk.END)
        self.corrected_aft_entry.delete(0, tk.END)
        self.corrected_mid_entry.delete(0, tk.END)

        self.obs_trim_entry.insert(tk.END, str(trim_observed))
        self.lbm_entry.insert(tk.END, str(lbm))
        self.corrected_for_entry.insert(tk.END, str(draft_for_corrected))
        self.corrected_aft_entry.insert(tk.END, str(draft_aft_corrected))
        self.corrected_mid_entry.insert(tk.END, str(draft_mid_corrected))
        self.result_lbl.configure(text="Success")

        # MFA / MOM / QM :
        mfa = ""
        mom = ""
        qm = ""

        mfa = round((draft_for_corrected + draft_aft_corrected) / 2, 2)
        mom = round((mfa + draft_mid_corrected) / 2, 2)
        qm = round((mom + draft_mid_corrected) / 2, 2)

        self.mean_for_aft_entry.delete(0, tk.END)
        self.mean_of_mean_entry.delete(0, tk.END)
        self.quarter_mean_entry.delete(0, tk.END)
        self.init_draft_entry.delete(0, tk.END)

        self.mean_for_aft_entry.insert(tk.END, str(mfa))
        self.mean_of_mean_entry.insert(tk.END, str(mom))
        self.quarter_mean_entry.insert(tk.END, str(qm))
        self.init_draft_entry.insert(tk.END, str(qm))

        self.obs_trim_entry.configure(state=DISABLED)
        self.lbm_entry.configure(state=DISABLED)
        self.init_draft_entry.configure(state=DISABLED)
        self.corrected_for_entry.configure(state=DISABLED)
        self.corrected_aft_entry.configure(state=DISABLED)
        self.corrected_mid_entry.configure(state=DISABLED)
        self.mean_for_aft_entry.configure(state=DISABLED)
        self.mean_of_mean_entry.configure(state=DISABLED)
        self.quarter_mean_entry.configure(state=DISABLED)
        self.init_draft_entry.configure(state=DISABLED)

        # return self.frame_content


class ThirdPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        load = Image.open("p3.jpg")
        photo = ImageTk.PhotoImage(load)
        label = tk.Label(self, image=photo)
        label.image = photo
        label.place(x=0, y=0)

        # lbl = tk.Label(self, text='ThirdPage', font=('Arial', 12, 'bold'))
        # lbl.place(x=222, y=260)
        btn = tk.Button(self, text='Home', font=('Arial', 16, 'bold'), command=lambda: controller.show_frame(FirstPage))
        btn.place(x=452, y=360)
        btn = tk.Button(self, text='Back', font=('Arial', 16, 'bold'),
                        command=lambda: controller.show_frame(SecondPage))
        btn.place(x=252, y=360)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, *kwargs)
        # creation of a window
        window = tk.Frame(self)
        window.pack()

        window.grid_rowconfigure(0, minsize=1000)
        window.grid_columnconfigure(0, minsize=1320)

        self.frames = {}
        for F in (FirstPage, SecondPage, ThirdPage):
            frame = F(window, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
        self.show_frame(FirstPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()


app = Application()
app.maxsize(1320, 1000)
app.state('zoomed')
app.mainloop()
