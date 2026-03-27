from view.ViewStatistic import ViewStatistic

from model.statistics_model import StatisticsStockModel
from model.stock_db_model import SQLconnect

from controller.base_controller import BaseController

import customtkinter as ct
class ControllerStatistic(BaseController):
    def __init__(
        self, master, dsc, leksykon_programu, konfiguracja_programu, 
        sound=None, 
        messagebox_controller=None, 
        language_code=None,
        main_controller=None,
        all_currency=None
    ):
        super().__init__(konfiguracja_programu, all_currency)

        self.session = SQLconnect()
        self.stats_model = StatisticsStockModel(self.session)

        self.master = master
        self.dsc = dsc
        self.leksykon_programu = leksykon_programu
        self.main_controller = main_controller
        self.sound = sound
        self.messagebox_controller = messagebox_controller
        self.language_code = language_code

        self.statistic_master = ct.CTkToplevel(self.master)

        self.view = ViewStatistic(
            self.statistic_master, 
            dsc=self.dsc, 
            leksykon=self.leksykon_programu, 
            konfiguracja_programu=self.konfiguracja_programu, 
            language_code=self.language_code,
            sound=self.sound
        )

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
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_category", {"text": "Category Stats", "toolTip": ""})
        self.view.utworz_przycisk(frame, self.open_statistic_category, leksykon_programu=leksykon, icon=self.view.category_icon)

    def button_company_stats(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_company", {"text": "Company Stats", "toolTip": ""})
        self.view.utworz_przycisk(frame, self.open_statistic_company, leksykon_programu=leksykon, icon=self.view.company_icon)

    def button_buyers_stats(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_buyers", {"text": "Buyers Stats", "toolTip": ""})
        self.view.utworz_przycisk(frame, self.open_statistic_buyers, leksykon_programu=leksykon, icon=self.view.buyers_icon)

    def button_shops_stats(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_shops", {"text": "Shops Stats", "toolTip": ""})
        self.view.utworz_przycisk(frame, self.open_statistic_shops, leksykon_programu=leksykon, icon=self.view.shops_icon)

    def button_artykuly_stats(self, frame):
        leksykon = self.leksykon_programu.get("buttons", {}).get("button_artykuly", {"text": "Arts Stats", "toolTip": ""})
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

