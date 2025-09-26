import tkinter as tk

from view.ViewOrder import ViewOrder
from model.stock_db_model import SQLconnect


class ControllerOrder:    
    def __init__(
            self, master, dsc, leksykon_programu, leksykon_messagebox, konfiguracja_programu, 
            sound = None, 
            messagebox_controller = None, 
            currency = None, 
            language_code = None, 
            main_controller=None
            ):
        
        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.leksykon_messagebox = leksykon_messagebox
        self.konfiguracja_programu = konfiguracja_programu
        self.currency = currency
        self.main_controller = main_controller

        self.order_master = tk.Toplevel(master)
        self.db_session = SQLconnect()

        self.view = ViewOrder(
            self.order_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            currency=self.currency,
            konfiguracja_programu=konfiguracja_programu, 
            language_code=language_code,
            sound=sound
            )

        self.messagebox_controller = messagebox_controller 
        self.inicjalizacja_frame()

        self.button_manager(frame="main", startup = True)

        self.order_master.protocol("WM_DELETE_WINDOW", self.on_closing_order_window)

    def run(self):
        self.order_master.deiconify()

    def close(self):
        if self.db_session:
            self.db_session.close()
            self.db_session = None

    def on_closing_order_window(self):
        if self.messagebox_controller.close_info():
            self.close()
            if self.order_master.winfo_exists():
                self.order_master.destroy()
            if self.main_controller:
                self.main_controller.close_stock_window()

    def inicjalizacja_frame(self):
        self.button_orders_frame = self.view.button_orders_frame
        self.order_frame = self.view.order_frame
        self.secend_frame = self.view.secend_frame

    def button_manager(self, frame = None, back_target = 'main', startup = False):
        if startup == False:
            for widget in self.order_frame.winfo_children():
                widget.destroy()

            for widget in self.button_orders_frame.winfo_children():
                widget.destroy()

        if frame == "main":
            self.button_test(self.button_orders_frame)


    def button_test(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, print("nic"), icon=self.view.buyers_icon, leksykon_programu=leksykon)
