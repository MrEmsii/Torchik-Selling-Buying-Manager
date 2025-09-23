import tkinter as tk
from view.ViewStatistic import ViewStatistic
from model.statistics_model import StatisticsStockModel
from model.stock_db_model import SQLconnect

class ControllerStatistic:
    def __init__(
            self, master, dsc, leksykon_programu, konfiguracja_programu, 
            sound = None, 
            messagebox_controller = None, 
            currency = None, 
            language_code = None,
            main_controller=None
            ):
        db_session = SQLconnect()
        self.session = db_session
        self.stats_model = StatisticsStockModel(db_session)

        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.konfiguracja_programu = konfiguracja_programu
        self.currency = currency
        self.main_controller = main_controller


        self.statistic_master = tk.Toplevel(master)

        self.view = ViewStatistic(
            self.statistic_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            konfiguracja_programu=konfiguracja_programu, 
            language_code=language_code
            )

        self.sound = sound
        self.messagebox_controller = messagebox_controller 
        self.inicjalizacja_frame()

        self.button_manager()

        self.statistic_master.protocol("WM_DELETE_WINDOW", self.on_closing_order_window)


    def run(self):
        self.statistic_master.deiconify()

    def close(self):
        if self.session:
            self.session.close()
            self.session = None

    def on_closing_order_window(self):
        if self.messagebox_controller.close_info():
            self.close()
            if self.statistic_master.winfo_exists():
                self.statistic_master.destroy()
            if self.main_controller:
                self.main_controller.close_statistic_window()

    def inicjalizacja_frame(self):
        self.statisic_frame = self.view.statistic_frame
        self.table_frame = self.view.table_frame
        self.button_statistic_frame = self.view.button_statistic_frame

    def button_manager(self):
        self.button_category_stats(self.button_statistic_frame)
        self.button_company_stats(self.button_statistic_frame)
        self.button_buyers_stats(self.button_statistic_frame)
        self.button_shops_stats(self.button_statistic_frame)
        self.button_artykuly_stats(self.button_statistic_frame)


    def button_category_stats(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_category"]
        self.view.utworz_przycisk(frame, self.open_statistic_category, leksykon_programu=leksykon, icon=self.view.category_icon)

    def button_company_stats(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_company"]
        self.view.utworz_przycisk(frame, self.open_statistic_company, leksykon_programu=leksykon, icon=self.view.company_icon)

    def button_buyers_stats(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_buyers"]
        self.view.utworz_przycisk(frame, self.open_statistic_buyers, leksykon_programu=leksykon, icon=self.view.buyers_icon)

    def button_shops_stats(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_shops"]
        self.view.utworz_przycisk(frame, self.open_statistic_shops, leksykon_programu=leksykon, icon=self.view.shops_icon)

    def button_artykuly_stats(self, frame):
        leksykon = self.leksykon_programu["buttons"]["button_artykuly"]
        self.view.utworz_przycisk(frame, self.open_statistic_arts, leksykon_programu=leksykon, icon=self.view.arts_icon)


    def open_statistic_arts(self):
        koszty = self.stats_model.koszt_artykulow()
        self.view.update_table(["Artykuł", "Koszt"], koszty)
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt artykułów", 
            master=self.statisic_frame
        )

    def open_statistic_company(self):
        koszty = self.stats_model.koszt_w_firma()
        self.view.update_table(["Firma", "Koszt"], koszty)
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w firmach", 
            master=self.statisic_frame
        )

    def open_statistic_buyers(self):
        koszty = self.stats_model.koszt_w_kupujacych()
        self.view.update_table(["Kupujący", "Koszt"], koszty)
        self.view.show_chart_pie(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w kupujacych", 
            master=self.statisic_frame
        )

    def open_statistic_shops(self):
        koszty = self.stats_model.koszt_w_sklepach()
        self.view.update_table(["Sklep", "Koszt"], koszty)
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w sklepach", 
            master=self.statisic_frame
        )

    def open_statistic_category(self):
        koszty = self.stats_model.koszt_w_kategori()
        self.view.update_table(["Kategoria", "Koszt"], koszty)
        self.view.show_chart(
            labels=[nazwa for nazwa, _ in koszty],
            values=[total for _, total in koszty],
            title="Koszt wygenerowany w kategorii", 
            master=self.statisic_frame
        )

