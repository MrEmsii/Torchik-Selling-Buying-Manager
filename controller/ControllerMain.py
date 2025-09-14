from view.ViewMessageBox import ViewMessageBox
 
class ControllerMain:
    def __init__(self):
        #wczytanie słowników, podzielenie słowników na elementy, 
        #uruchomienie okna głównego z możliwością wybory dalszego działania
        #wybór między zamówienia, statystyki
        pass

    def run(self):
        pass
    
    def on_closing(self):
        leksykon = self.leksykon_programu["close_messagebox"]
                
        if ViewMessageBox.messagebox(self, type="close", heading=leksykon["heading"], text=leksykon["text"]):
            self.view.master.destroy()