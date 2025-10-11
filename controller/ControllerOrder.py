import threading
import tkinter as tk

from sqlalchemy import select

from view.ViewOrder import ViewOrder
from model.order_db_model import SQLconnect, Kupujacy, Zamowienie, Artykul_Lista, Faktury, artykuly_relacja

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
        self.sound = sound

        self.order_master = tk.Toplevel(master)
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

        self.messagebox_controller = messagebox_controller 
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
            if self.main_controller:
                self.main_controller.close_order_window()

    def inicjalizacja_frame(self):
        self.button_orders_frame = self.view.button_orders_frame
        self.order_frame = self.view.order_frame
        self.realizacja_frame = self.view.realizacja_frame

    def show_message_async(self):
        self.messagebox_controller.show_message_async(master=self.order_master)

    def hide_message_async(self):
        self.messagebox_controller.ukryj_message_async(master=self.order_master)

    def button_manager(self, frame = None, back_target = 'main', startup = False):
        if startup == False:
            for widget in self.order_frame.winfo_children():
                widget.destroy()

            for widget in self.button_orders_frame.winfo_children():
                widget.destroy()

        if frame == "list_zamowienia":
            self.button_test(self.button_orders_frame)
        elif frame == "list_inside_order":
            self.button_back(self.button_orders_frame) 

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
        
        self.load_inside(id_zamowienia)
        self.load_more_info(id_zamowienia)

    def load_more_info(self, id_zamowienia):
        info_columns = ["data wysyłki, rabat j, rabat %, koszta, faktura nr, cena całkowita, cena po rabacie, kupujący, nazwa zamówienia"]
        self.inside_more_tree.delete(*self.inside_more_tree.get_children())
        zamowienie = self.db_session.query(Zamowienie).filter_by(id=id_zamowienia).first()
        if zamowienie:
            data_wysylki = zamowienie.data_wysylki if zamowienie.data_wysylki else " "
            rabat_j = f"{zamowienie.rabat_j:,.2f} {self.currency}".replace(",", " ") if zamowienie.rabat_j else "0"
            rabat_proc = f"{zamowienie.rabat_procent} %" if zamowienie.rabat_procent else "0 %"
            koszta = f"{zamowienie.oblicz_koszta(self.db_session):,.2f} {self.currency}".replace(",", " ") if zamowienie.oblicz_koszta(self.db_session) else "0"
            faktura_nr = zamowienie.faktura.faktura_nr if zamowienie.faktura else " "
            cena_calkowita = f"{zamowienie.oblicz_przychod(self.db_session):,.2f} {self.currency}".replace(",", " ") if zamowienie.oblicz_przychod(self.db_session) else "0"
            cena_po_rabacie = f"{zamowienie.oblicz_dochod(self.db_session):,.2f} {self.currency}".replace(",", " ") if zamowienie.oblicz_dochod(self.db_session) else "0"
            kupujacy = zamowienie.kupujacy.nazwa if zamowienie.kupujacy else " "
            nazwa_zamowienia = zamowienie.nazwa_zamowienia if zamowienie.nazwa_zamowienia else " "

            self.inside_more_tree.insert('', 'end', iid=1, values=("Data wysyłki: ", data_wysylki))
            self.inside_more_tree.insert('', 'end', iid=2, values=("Rabat j: ", rabat_j))
            self.inside_more_tree.insert('', 'end', iid=3, values=("Rabat %: ", rabat_proc))
            self.inside_more_tree.insert('', 'end', iid=4, values=("Koszta: ", koszta))
            self.inside_more_tree.insert('', 'end', iid=5, values=("Faktura nr: ", faktura_nr))
            self.inside_more_tree.insert('', 'end', iid=6, values=("Cena całkowita: ", cena_calkowita))
            self.inside_more_tree.insert('', 'end', iid=7, values=("Cena po rabacie: ", cena_po_rabacie))
            self.inside_more_tree.insert('', 'end', iid=8, values=("Kupujący: ", kupujacy))
            self.inside_more_tree.insert('', 'end', iid=9, values=("Nazwa zamówienia: ", nazwa_zamowienia))
        else:
            print(f"Nie znaleziono zamówienia o ID {id_zamowienia}")

    def load_inside(self, id_zamowienia):
        wynik_all = self.db_session.execute(
            select(
                artykuly_relacja.c.artykul_id,
                artykuly_relacja.c.ilosc_artykulu,
                artykuly_relacja.c.czas_druku_1_elem,
                artykuly_relacja.c.waga_1_elem,
                artykuly_relacja.c.koszt_1kg_materialu,
                artykuly_relacja.c.cena_1_elem
            )
            .where(
                artykuly_relacja.c.zamowienie_id == id_zamowienia
                )
        ).fetchall()

        existing_iids = set(self.inside_tree.get_children())

        artykul_data = []

        for wynik in wynik_all:
            id_art = wynik.artykul_id
            waga_1_elem = float(f"{wynik.waga_1_elem if wynik.waga_1_elem else 0:.2f}")
            koszt_1kg = float(f"{wynik.koszt_1kg_materialu if wynik.koszt_1kg_materialu else 0:.2f}")
            koszt_1_elem = waga_1_elem*koszt_1kg
            czas_druku_1_elem = float(wynik.czas_druku_1_elem if wynik.czas_druku_1_elem else 0)
            ilosc = int(wynik.ilosc_artykulu if wynik.ilosc_artykulu else 1)
            cena_1_elem = float(f"{wynik.cena_1_elem if wynik.cena_1_elem else 0:.2f}")

            cena_calkowita = round(ilosc*cena_1_elem, 2) if cena_1_elem else 0
            waga_calkowita = round(ilosc*waga_1_elem, 2) if waga_1_elem else 0
            czas_calkowity = round(ilosc*czas_druku_1_elem, 2) if czas_druku_1_elem else 0
            koszt_calkowity = round(waga_calkowita*koszt_1kg, 2) if waga_calkowita else 0

            artykul = self.db_session.query(Artykul_Lista).filter_by(id=id_art).first()
            nazwa = artykul.nazwa

            unique_id = f"{id_art}-{ilosc}-{czas_druku_1_elem}-{waga_1_elem}"
            counter = 1
            while unique_id in existing_iids:
                unique_id = f"{id_art}-{ilosc}-{czas_druku_1_elem}-{waga_1_elem}-{counter}"
                counter += 1

            cena_1_elem = f"{cena_1_elem:,.2f} {self.currency}".replace(",", " ")
            koszt_1_elem = f"{koszt_1_elem:,.2f} {self.currency}".replace(",", " ") 
            waga_1_elem = f"{waga_1_elem} kg"

            waga_calkowita = f"{waga_calkowita} kg"
            cena_calkowita = f"{cena_calkowita:,.2f} {self.currency}".replace(",", " ")
            koszt_calkowity = f"{koszt_calkowity:,.2f} {self.currency}".replace(",", " ")
            czas_calkowity = f"{int(czas_calkowity)} h {int((czas_calkowity - int(czas_calkowity))*60)} min" if czas_calkowity >=1 else f"{int(czas_calkowity*60)} min"
            czas_druku_1_elem = f"{int(czas_druku_1_elem)} h {int((czas_druku_1_elem - int(czas_druku_1_elem))*60)} min" if czas_druku_1_elem >=1 else f"{int(czas_druku_1_elem*60)} min"

            existing_iids.add(unique_id)
            artykul_data.append((id_art, nazwa, czas_druku_1_elem, waga_1_elem, koszt_1_elem, cena_1_elem, ilosc, waga_calkowita, czas_calkowity, koszt_calkowity, cena_calkowita))

        artykul_data.sort(key=lambda x: x[2])

        for row in artykul_data:
            self.inside_tree.insert('', 'end', iid=row[0], values=row[1:])

    def load_realizacja_daemon(self, widok = "ukryj"):
        print("load_statusy_daemon")
        commend = self.load_realizacja(widok = widok)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_order_daemon(self, widok = "ukryj"):
        print("load_orders_daemon")
        commend = self.load_zamowienia(widok = widok)
        threading.Thread(target=lambda: commend, daemon=True).start()

    def load_zamowienia(self, widok = "ukryj", realziacja_id=None):
        if widok == "pokaz":
            self.show_message_async()

        def task():

            if not realziacja_id:
                zamowienia = self.db_session.query(Zamowienie).all()
            else:
                zamowienia = self.db_session.query(Zamowienie).filter_by(realizacja_id=realziacja_id).all()
            
            zamowienia_data = []

            for zamow in zamowienia:
                zamow_id = zamow.id
                zamow_realizacja_id = zamow.realizacja_id if zamow.realizacja_id else 0
                zamow_realizacja = self.leksykon_programu["implementation_state"][zamow_realizacja_id]
                zamow_data_zlozenia_zamow = zamow.data_zlozenia_zamowienia if zamow.data_zlozenia_zamowienia else None
                zamow_data_deadline = zamow.data_deadline if zamow.data_deadline else None
                zamow_kupujacy = zamow.kupujacy.nazwa if zamow.kupujacy else " "
                zamow_nazwa_zamowienia = zamow.nazwa_zamowienia if zamow.nazwa_zamowienia else None

                zamow_cena = f"{zamow.oblicz_przychod(self.db_session):,.2f} {self.currency}".replace(",", " ")
                zamow_cena_rabat = f"{zamow.oblicz_dochod(self.db_session):,.2f} {self.currency}".replace(",", " ")
                
                realizacja_id = zamow.realizacja_id

                zamowienia_data.append((zamow_id, zamow_realizacja, zamow_data_zlozenia_zamow, zamow_data_deadline, zamow_kupujacy, zamow_nazwa_zamowienia, zamow_cena, zamow_cena_rabat, realizacja_id))

            zamowienia_data.sort(key=lambda x: x[2], reverse=True)
            zamowienia_data.sort(key=lambda x: x[8], reverse=False)

            def update_gui():
                self.zamowienia_tree.delete(*self.zamowienia_tree.get_children())
                for zamow_id, zamow_realizacja, zamow_data_zlozenia_zamow, zamow_data_deadline, zamow_kupujacy, zamow_nazwa_zamowienia, zamow_cena, zamow_cena_rabat, realizacja_id in zamowienia_data:
                    self.zamowienia_tree.insert('', 'end', values=(zamow_id, zamow_realizacja, zamow_data_zlozenia_zamow, zamow_data_deadline, zamow_kupujacy, zamow_nazwa_zamowienia, zamow_cena, zamow_cena_rabat, realizacja_id))
                if widok == "pokaz": self.hide_message_async()

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
