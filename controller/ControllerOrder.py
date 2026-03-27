import threading

import customtkinter as ct

from sqlalchemy import select

from view.ViewOrder import ViewOrder
from model.order_db_model import SQLconnect, Kupujacy, Zamowienie, Artykul_Lista, Faktury, ListaDodanie

from sqlalchemy.orm import joinedload

from controller.base_controller import BaseController

class ControllerOrder(BaseController):    
    def __init__(
        self, master, dsc, leksykon_programu, konfiguracja_programu, 
        sound=None, 
        messagebox_controller=None, 
        language_code=None, 
        main_controller=None,
        all_currency=None
    ):
        super().__init__(konfiguracja_programu, all_currency)

        self.master = master
        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.main_controller = main_controller
        self.sound = sound
        self.messagebox_controller = messagebox_controller
        self.language_code = language_code

        self.order_master = ct.CTkToplevel(self.master)

        self.db_session = SQLconnect()

        self.view = ViewOrder(
            self.order_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            konfiguracja_programu=self.konfiguracja_programu, 
            language_code=self.language_code,
            sound=self.sound
        )

        self.inicjalizacja_frame()
        self.list_zamowienia()

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

    def inicjalizacja_frame(self):
        self.button_orders_frame = self.view.button_orders_frame
        self.order_frame = self.view.order_frame
        self.realizacja_frame = self.view.realizacja_frame

    def show_message_async(self):
        self.messagebox_controller.show_message_async(master=self.order_master)

    def hide_message_async(self):
        self.messagebox_controller.hide_message_async(master=self.order_master)

    def button_manager(self, frame=None, back_target='main', startup=False):
        if not startup:
            for f in (self.order_frame, self.button_orders_frame):
                for widget in f.winfo_children():
                    widget.destroy()

        buttons = {
            "list_zamowienia": lambda: self.button_test(self.button_orders_frame),
            "list_inside_order": lambda: self.button_back(self.button_orders_frame)
        }
        buttons.get(frame, lambda: None)()

    def button_test(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_test", "Test")
        self.view.utworz_przycisk(frame, lambda: print("nic"), icon=self.view.buyers_icon, leksykon_programu=leksykon)

    def button_back(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_back", "Powrót")
        self.view.utworz_przycisk(frame, self.list_zamowienia, icon=self.view.buyers_icon, leksykon_programu=leksykon)

    def list_zamowienia(self):
        self.usun_all_widgets()
        self.view.order_grid_setting()
        self.button_manager(frame="list_zamowienia", startup = True)
        order_heading = self.leksykon_programu["names_list"]["order"]
        status_heading = self.leksykon_programu["names_list"]["rezalizacja_status"]
        self.zamowienia_tree = self.view.order_tree(parent_frame=self.order_frame, label_text=order_heading) 
        self.realiacja_tree = self.view.realizacja_tree(parent_frame=self.realizacja_frame, label_text=status_heading) 
        self.load_realizacja_daemon()
        self.load_order_daemon(widok="pokaz")
        
        self.realiacja_tree.bind("<Double-1>", self.on_double_click_filtrowanie_status)
        self.realiacja_tree.bind("<Double-3>", self.on_double_click_filtrowanie_status_resetowanie)

        self.zamowienia_tree.bind("<Double-1>", self.on_double_click_otwieranie_zamowienia)

    def list_inside_order(self, id_zamowienia):
        self.usun_all_widgets()

        self.view.inside_grid_setting()

        self.button_manager(frame="list_inside_order", startup = False)
        column_heading = self.leksykon_programu["names_list"]["list_added_to_order"]
        more_info_column_heading = self.leksykon_programu["names_list"]["more_info_in_order"]

        self.inside_tree = self.view.inside_tree(parent_frame=self.order_frame, label_text=column_heading) 
        self.inside_more_tree = self.view.info_tree(parent_frame=self.realizacja_frame, label_text=more_info_column_heading)
        self.inside_tree.delete(*self.inside_tree.get_children())
        
        self.load_inside_daemon(id_zamowienia)
        self.load_more_info_daemon(id_zamowienia)

    def load_realizacja_daemon(self, widok = "ukryj"):
        print("Wczytywanie realizacji...")
        threading.Thread(target=lambda: self.load_realizacja(widok = widok), daemon=True).start()

    def load_order_daemon(self, widok = "ukryj"):
        print("Wczytywanie zamówień...")
        threading.Thread(target=lambda: self.load_zamowienia(widok = widok), daemon=True).start()

    def load_inside_daemon(self, id_zamowienia):
        print("Wczytywanie szczegółów zamówienia...")
        threading.Thread(target=lambda: self.load_inside(id_zamowienia), daemon=True).start()

    def load_more_info_daemon(self, id_zamowienia):
        print("Wczytywanie dodatkowych informacji...")
        threading.Thread(target=lambda: self.load_more_info(id_zamowienia), daemon=True).start()

    def load_more_info(self, id_zamowienia):
        self.inside_more_tree.clear()

        zamowienie = self.db_session.query(Zamowienie).filter_by(id=id_zamowienia).first()
        if not zamowienie:
            return

        koszta_val = zamowienie.oblicz_koszta() or 0
        przychod_val = zamowienie.oblicz_przychod() or 0
        dochod_val = zamowienie.oblicz_dochod() or 0

        info_data = [
            ("Data wysyłki:", zamowienie.data_wysylki or "-"),
            ("Rabat j:", self.currency_format(zamowienie.rabat_j)),
            ("Rabat %:", f"{zamowienie.rabat_procent or 0} %"),
            ("Koszta:", self.currency_format(koszta_val)),
            ("Faktura nr:", zamowienie.faktura.faktura_nr if zamowienie.faktura else "-"),
            ("Cena całkowita:", self.currency_format(przychod_val)),
            ("Cena po rabacie:", self.currency_format(dochod_val)),
            ("Kupujący:", zamowienie.kupujacy.nazwa if zamowienie.kupujacy else "-"),
            ("Nazwa:", zamowienie.nazwa_zamowienia or "-"),
            ("Opis:", zamowienie.opis_zamowienia or "-")
        ]

        self.inside_more_tree.insert_rows_bulk(info_data)

    def load_inside(self, id_zamowienia):
        zam = self.db_session.query(Zamowienie).options(joinedload(Zamowienie.pozycje).joinedload(ListaDodanie.artykul)).get(id_zamowienia)
        if not zam or not zam.pozycje:
            return

        existing_iids = set(self.inside_tree.get_children())

        def format_czas(godziny: float) -> str:
            if godziny >= 1:
                h = int(godziny)
                m = int((godziny - h) * 60)
                return f"{h} h {m} min"
            return f"{int(godziny * 60)} min"

        artykul_data = []
        for p in zam.pozycje:
            id_art = p.artykul_id
            ilosc = int(p.ilosc_artykulu or 1)
            waga_1_elem = round(p.waga_1_elem or 0, 2)
            koszt_1kg = round(p.koszt_1kg_materialu or 0, 2)
            koszt_1_elem = round(waga_1_elem * koszt_1kg, 2)
            czas_druku_1_elem = float(p.czas_druku_1_elem or 0)
            cena_1_elem_val = round(p.cena_1_elem or 0, 2)

            cena_calkowita_val = round(ilosc * cena_1_elem_val, 2)
            waga_calkowita_val = round(ilosc * waga_1_elem, 2)
            czas_calkowity_val = round(ilosc * czas_druku_1_elem, 2)
            koszt_calkowity_val = round(waga_calkowita_val * koszt_1kg, 2)

            nazwa = p.artykul.nazwa if p.artykul else "Nieznany"

            unique_id = f"{id_art}-{ilosc}-{waga_1_elem}"
            counter = 1
            while unique_id in existing_iids:
                unique_id = f"{id_art}-{ilosc}-{waga_1_elem}-{counter}"
                counter += 1
            existing_iids.add(unique_id)

            artykul_data.append((
                unique_id,
                nazwa,
                format_czas(czas_druku_1_elem),
                f"{waga_1_elem:.2f} kg",
                self.currency_format(koszt_1_elem),
                self.currency_format(cena_1_elem_val),
                ilosc,
                f"{waga_calkowita_val:.2f} kg",
                format_czas(czas_calkowity_val),
                self.currency_format(koszt_calkowity_val),
                self.currency_format(cena_calkowita_val)
            ))

        artykul_data.sort(key=lambda x: x[2])

        for row in artykul_data:
            self.inside_tree.insert('', 'end', iid=row[0], values=row[1:])

    def load_zamowienia(self, widok="ukryj", realziacja_id=None):
        if widok == "pokaz":
            self.messagebox_controller.show_message_async(master=self.order_master)

        def task():
            query = self.db_session.query(Zamowienie).options(joinedload(Zamowienie.kupujacy))
            if realziacja_id:
                query = query.filter_by(realizacja_id=realziacja_id)
            zamowienia = query.all()

            progress_step = max(1, len(zamowienia) // 100)
            zamowienia_data = []

            for i, z in enumerate(zamowienia):
                implementation_state = self.leksykon_programu["implementation_state"]

                zamowienia_data.append((
                    z.id,
                    implementation_state[z.realizacja_id if z.realizacja_id and z.realizacja_id < len(implementation_state) else 0],
                    z.data_zlozenia_zamowienia,
                    z.data_deadline,
                    z.kupujacy.nazwa if z.kupujacy else " ",
                    z.nazwa_zamowienia,
                    self.currency_format(z.oblicz_koszta()),
                    self.currency_format(z.oblicz_dochod()),
                    z.realizacja_id,
                ))

                if i % progress_step == 0:
                    self.messagebox_controller.update_message_async(i / len(zamowienia))

            zamowienia_data.sort(key=lambda x: (x[8], -x[2].toordinal() if x[2] else 0))


            def update_gui():
                self.zamowienia_tree.delete(*self.zamowienia_tree.get_children())
                for row in zamowienia_data:
                    self.zamowienia_tree.insert('', 'end', values=row)
                if widok == "pokaz":
                    self.hide_message_async()

            self.order_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()

    def load_realizacja(self, widok = "ukryj", select_item = None):
        if widok == "pokaz":
            self.show_message_async()

        def task():
            statusy = self.leksykon_programu["implementation_state"]
            statusy_data = []

            for i, status in enumerate(statusy):
                statusy_data.append((i, status))

            def update_gui():
                self.realiacja_tree.delete(*self.realiacja_tree.get_children())
                for sklep_id, sklep_nazwa in statusy_data:
                    self.realiacja_tree.insert('', 'end', values=(sklep_id, sklep_nazwa))
                self.zaznacz_wiersz_z_wartoscia(self.realiacja_tree, 'id', select_item)
                if widok == "pokaz": self.hide_message_async()

            self.order_master.after(0, update_gui)

        threading.Thread(target=task, daemon=True).start()


    def zaznacz_wiersz_z_wartoscia(self, treeview, kolumna, wartosc):
        for item in treeview.get_children():
            if treeview.set(item, kolumna) == str(wartosc):
                treeview.selection_set(item)
                treeview.focus(item)
                treeview.see(item)
                break

    def on_double_click_filtrowanie_status(self, event):
        selected_item = self.realiacja_tree.selection()
        if selected_item:
            realziacja_id = self.realiacja_tree.item(selected_item[0], 'values')[0]
            self.load_realizacja(select_item=selected_item)
            self.load_zamowienia(realziacja_id=realziacja_id, widok="pokaz")

            self.sound.play_confirm_sound()


    def on_double_click_filtrowanie_status_resetowanie(self, event):
        self.load_realizacja()
        self.load_zamowienia(widok="pokaz")

        self.sound.play_confirm_sound()


    def on_double_click_otwieranie_zamowienia(self, event):
        selected_item = self.zamowienia_tree.selection()
        self.zamowienie_id = selected_item

        if selected_item:
            self.zamowienie_id = self.zamowienia_tree.item(selected_item[0], 'values')[0]
            self.list_inside_order(self.zamowienie_id)

            self.sound.play_confirm_sound()

    def usun_all_widgets(self):
        for widget in self.view.order_frame.winfo_children():
            widget.destroy()

        for widget in self.view.realizacja_frame.winfo_children():
            widget.destroy()

        for widget in self.view.button_orders_frame.winfo_children():
            widget.destroy()
