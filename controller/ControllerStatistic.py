import tkinter as tk
from view.ViewStatistic import ViewStatistic
from model.statistics_model import StatisticsModel
from model.db_model import SQLconnect

class ControllerStatistic:
    def __init__(self, master, dsc, leksykon_programu, konfiguracja_programu, sound = None, messagebox_controller = None, currency = None, language_code = None):
        db_session = SQLconnect()
        self.session = db_session
        self.stats_model = StatisticsModel(db_session)

        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.konfiguracja_programu = konfiguracja_programu
        self.currency = currency

        self.order_master = tk.Toplevel(master)
        # self.db_session = SQLconnect()

        self.view = ViewStatistic(
            self.order_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            konfiguracja_programu=konfiguracja_programu, 
            language_code=language_code
            )

        self.sound = sound
        self.messagebox_controller = messagebox_controller 
        self.inicjalizacja_frame()

        self.button_manager()

    def run(self):
        self.view.statistic_master.protocol("WM_DELETE_WINDOW", self.on_closing_order_window)
        self.view.statistic_master.mainloop()

    def on_closing_order_window(self):
        if self.messagebox_controller.close_info():
            self.view.statistic_master.destroy() 

    def inicjalizacja_frame(self):
        self.statisic_frame = self.view.statistic_frame
        self.button_statistic_frame = self.view.button_statistic_frame

    def button_manager(self):
        self.button_category_stats(self.button_statistic_frame)
        self.button_company_stats(self.button_statistic_frame)
        self.button_buyers_stats(self.button_statistic_frame)
        self.button_shops_stats(self.button_statistic_frame)


    def button_category_stats(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, self.open_statistic_category, leksykon_programu=leksykon)

    def button_company_stats(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, self.open_statistic_company, leksykon_programu=leksykon)

    def button_buyers_stats(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, self.open_statistic_buyers, leksykon_programu=leksykon)

    def button_shops_stats(self, frame):
        leksykon = self.leksykon_programu["button_dodaj_zamowienie"]
        self.view.utworz_przycisk(frame, self.open_statistic_shops, leksykon_programu=leksykon)



    def open_statistic_company(self):
        koszty = self.stats_model.koszt_w_firma()
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w firmach", 
            master=self.statisic_frame
        )

    def open_statistic_buyers(self):
        koszty = self.stats_model.koszt_w_kupujacych()
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w kupujacych", 
            master=self.statisic_frame
        )

    def open_statistic_shops(self):
        koszty = self.stats_model.koszt_w_sklepach()
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w sklepach", 
            master=self.statisic_frame
        )

    def open_statistic_category(self):
        koszty = self.stats_model.koszt_w_kategori()
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w kategorii", 
            master=self.statisic_frame
        )



    def open_statistics_window(self, root):
        win = tk.Toplevel(root)
        win.title("Statystyki artykułów")
        win.geometry("800x600")

        self.view = ViewStatistic(win)

        # Koszt artykułów
        koszty = self.stats_model.srednia_cena_artykulu()
        self.view.update_table(["Artykuł", "Koszt"], koszty)
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt artykułów"
        )
        # Średnia cena
        srednie = self.stats_model.srednia_cena_artykulu()
        print("\nŚrednia cena artykułów:")
        for nazwa, avg in srednie:
            print(f"{nazwa}: {avg:.2f} zł")

        # Najdroższa firma
        firma = self.stats_model.firma_najwiekszy_koszt()
        print(f"\nFirma z największym kosztem: {firma[0]} ({firma[1]} zł)")

        # Najpopularniejsza kategoria
        kategoria = self.stats_model.najpopularniejsza_kategoria()
        print(f"\nNajpopularniejsza kategoria: {kategoria[0]} "
              f"({kategoria[1]} artykułów, koszt: {kategoria[2]} zł)")

