
class BaseController:
    def __init__(self, konfiguracja_programu=None, all_currency=None):
        self.konfiguracja_programu = konfiguracja_programu
        self.all_currency = all_currency
        
        print(f"Currency code: {self.currency_code}, symbol: {self.symbol}, symbol_first: {self.symbol_first}")

    @property
    def currency_code(self):
        return self.konfiguracja_programu.get("currency_code")

    @property
    def symbol(self):
        return self.all_currency.get(self.currency_code, {}).get("symbol")

    @property
    def symbol_first(self):
        return self.all_currency.get(self.currency_code, {}).get("symbol_first")

    def currency_format(self, value):
        if value is None:
            formatted_value = "0.00"
        else:
            formatted_value = f"{value:,.2f}".replace(",", ".")

        if self.symbol_first == 1:
            return f"{self.symbol} {formatted_value}"
        else:
            return f"{formatted_value} {self.symbol}"

    def currency_format_no_symbol(self, value):
        if value is None:
            return "0.00"

        if isinstance(value, str) and self.symbol:
            return value.replace(self.symbol, "").strip()

        return f"{value:,.2f}".replace(",", ".")

    # def currency_format(self, value):
    #     formatted_value = f"{value:,.2f}".replace(",", " ")
    #     if value is None:
    #         formatted_value = "0.00"
            
    #     if self.symbol_first:
    #         return f"{self.symbol} {formatted_value}"
    #     else:
    #         return f"{formatted_value} {self.symbol}"
        
    # def currency_format_no_symbol(self, value):
    #     if value is None:
    #         return "0.00"
    #     elif self.symbol in value:
    #         return value.replace(self.symbol, "").strip()
        
        