import threading
import tkinter as tk

import addons.customtkinter as ct

from sqlalchemy import select

from view.ViewOrder import ViewOrder
from model.order_db_model import SQLconnect, Kupujacy, Zamowienie, Artykul_Lista, Faktury, artykuly_relacja

from sqlalchemy.orm import joinedload

class ControllerOrder:    
    def __init__(
            self, master, dsc, leksykon_programu, konfiguracja_programu, 
            sound = None, 
            messagebox_controller = None, 
            currency = None, 
            language_code = None, 
            main_controller=None
            ):
        
        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.konfiguracja_programu = konfiguracja_programu
        self.currency = currency
        self.main_controller = main_controller
        self.sound = sound
        self.messagebox_controller = messagebox_controller 

        self.order_master = ct.CTkToplevel(master)
        self.db_session = SQLconnect()

        self.view = ViewOrder(
            self.order_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            currency=self.currency,
            konfiguracja_programu=konfiguracja_programu, 
            language_code=language_code,
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
        leksykon = self.leksykon_programu["buttons"]["button_test"]
        self.view.utworz_przycisk(frame, lambda: print("nic"), icon=self.view.buyers_icon, leksykon_programu=leksykon)

    def button_back(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_back"]
        self.view.utworz_przycisk(frame, self.list_zamowienia, icon=self.view.buyers_icon, leksykon_programu=leksykon)

    def list_zamowienia(self):
        self.usun_all_widgets()
        self.view.order_grid_setting()
        self.button_manager(frame="list_zamowienia", startup = True)
        order_heading = self.leksykon_programu["names_list"]["order"]
        status_heading = self.leksykon_programu["names_list"]["rezalizacja_status"]
        self.zamowienia_tree = self.view.order_tree(parent_frame=self.order_frame, label_text=order_heading) 
        self.realiacja_tree = self.view.name_tree(parent_frame=self.realizacja_frame, label_text=status_heading) 
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
        print("load_statusy_daemon")
        threading.Thread(target=lambda: self.load_realizacja(widok = widok), daemon=True).start()

    def load_order_daemon(self, widok = "ukryj"):
        print("load_orders_daemon")
        threading.Thread(target=lambda: self.load_zamowienia(widok = widok), daemon=True).start()

    def load_inside_daemon(self, id_zamowienia):
        print("load_inside_daemon")
        threading.Thread(target=lambda: self.load_inside(id_zamowienia), daemon=True).start()

    def load_more_info_daemon(self, id_zamowienia):
        print("load_more_info_daemon")
        threading.Thread(target=lambda: self.load_more_info(id_zamowienia), daemon=True).start()

    def load_more_info(self, id_zamowienia):
        # self.inside_more_tree.delete(*self.inside_more_tree.get_children())
        self.inside_more_tree.clear() #canvas

        zamowienie = self.db_session.query(Zamowienie).filter_by(id=id_zamowienia).first()
        if not zamowienie:
            print(f"Nie znaleziono zamówienia o ID {id_zamowienia}")
            return

        def format_money(value):
            return f"{value:,.2f} {self.currency}".replace(",", " ") if value else "0"

        def format_percent(value):
            return f"{value} %" if value else "0 %"

        koszta_val = zamowienie.oblicz_koszta(self.db_session) or 0
        przychod_val = zamowienie.oblicz_przychod(self.db_session) or 0
        dochod_val = zamowienie.oblicz_dochod(self.db_session) or 0

        data_wysylki = zamowienie.data_wysylki or " "
        rabat_j = format_money(zamowienie.rabat_j or 0)
        rabat_proc = format_percent(zamowienie.rabat_procent or 0)
        koszta = format_money(koszta_val)
        faktura_nr = zamowienie.faktura.faktura_nr if zamowienie.faktura else " "
        cena_calkowita = format_money(przychod_val)
        cena_po_rabacie = format_money(dochod_val)
        kupujacy = zamowienie.kupujacy.nazwa if zamowienie.kupujacy else " "
        nazwa_zamowienia = zamowienie.nazwa_zamowienia if zamowienie.nazwa_zamowienia else " "
        opis = zamowienie.opis_zamowienia if zamowienie.opis_zamowienia else ' '

        info_data = [
            ("Data wysyłki:", data_wysylki),
            ("Rabat j:", rabat_j),
            ("Rabat %:", rabat_proc),
            ("Koszta:", koszta),
            ("Faktura nr:", faktura_nr),
            ("Cena całkowita:", cena_calkowita),
            ("Cena po rabacie:", cena_po_rabacie),
            ("Kupujący:", kupujacy),
            ("Nazwa zamówienia:", nazwa_zamowienia),
            ("Opis zamówienia:", opis)
        ]

        # for i, (label, value) in enumerate(info_data, start=1):
        #     self.inside_more_tree.insert('', 'end', iid=i, values=(label, value))

        for label, value in info_data:
            self.inside_more_tree.insert_row(label, value)


    def load_inside(self, id_zamowienia):
        wynik_all = self.db_session.execute(
            select(
                artykuly_relacja.c.artykul_id,
                artykuly_relacja.c.ilosc_artykulu,
                artykuly_relacja.c.czas_druku_1_elem,
                artykuly_relacja.c.waga_1_elem,
                artykuly_relacja.c.koszt_1kg_materialu,
                artykuly_relacja.c.cena_1_elem
            ).where(artykuly_relacja.c.zamowienie_id == id_zamowienia)
        ).fetchall()

        if not wynik_all:
            return

        existing_iids = set(self.inside_tree.get_children())

        artykul_ids = [w.artykul_id for w in wynik_all]
        artykuly = (
            self.db_session.query(Artykul_Lista.id, Artykul_Lista.nazwa)
            .filter(Artykul_Lista.id.in_(artykul_ids))
            .all()
        )
        nazwy_artykulow = {a.id: a.nazwa for a in artykuly}

        def format_czas(godziny: float) -> str:
            """Konwertuj czas (w godzinach) do formatu 'X h Y min'."""
            if godziny >= 1:
                h = int(godziny)
                m = int((godziny - h) * 60)
                return f"{h} h {m} min"
            return f"{int(godziny * 60)} min"

        artykul_data = []
        for wynik in wynik_all:
            id_art = wynik.artykul_id
            ilosc = int(wynik.ilosc_artykulu or 1)
            waga_1_elem = round(wynik.waga_1_elem or 0, 2)
            koszt_1kg = round(wynik.koszt_1kg_materialu or 0, 2)
            koszt_1_elem = round(waga_1_elem * koszt_1kg, 2)
            czas_druku_1_elem = float(wynik.czas_druku_1_elem or 0)
            cena_1_elem_val = round(wynik.cena_1_elem or 0, 2)

            cena_calkowita_val = round(ilosc * cena_1_elem_val, 2)
            waga_calkowita_val = round(ilosc * waga_1_elem, 2)
            czas_calkowity_val = round(ilosc * czas_druku_1_elem, 2)
            koszt_calkowity_val = round(waga_calkowita_val * koszt_1kg, 2)

            nazwa = nazwy_artykulow.get(id_art, "Nieznany")

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
                f"{koszt_1_elem:,.2f} {self.currency}".replace(",", " "),
                f"{cena_1_elem_val:,.2f} {self.currency}".replace(",", " "),
                ilosc,
                f"{waga_calkowita_val:.2f} kg",
                format_czas(czas_calkowity_val),
                f"{koszt_calkowity_val:,.2f} {self.currency}".replace(",", " "),
                f"{cena_calkowita_val:,.2f} {self.currency}".replace(",", " ")
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
                    f"{z.oblicz_przychod(self.db_session):,.2f} {self.currency}".replace(",", " "),
                    f"{z.oblicz_dochod(self.db_session):,.2f} {self.currency}".replace(",", " "),
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
