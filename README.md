# SellingBuyingManager – System zarządzania zamówieniami

## 🧾 Opis

SellingBuyingManager to aplikacja desktopowa typu CRUD służąca do zarządzania zamówieniami, kupującymi, artykułami i produktami. Wykorzystuje SQLAlchemy do obsługi bazy danych SQLite oraz interfejs graficzny zbudowany w oparciu o Tkinter i tkinterDnD2. Relacje między obiektami odwzorowane są za pomocą modeli ORM.

Aplikacja wspiera import danych, posiada warstwę GUI z ikonami, tooltipami i kalendarzem, oraz system dźwiękowy do powiadomień.

---

## 🎯 Funkcje

* Tworzenie, edycja i usuwanie:
  * Kupujących
  * Sklepów
  * Firm
  * Kategorii
  * Artykułów
  * Zamówień
* Kategoryzacja artykułów
* Powiązanie artykułów z firmami i kategoriami
* Tworzenie zamówień z listą produktów, ilością i rabatami
* Obsługa dźwięków (kliknięcia, błędy, start)
* Obsługa JSON-ów z konfiguracją i językiem
* Obsługa danych z kalendarza (tkcalendar)

---

## 🗃️ Struktura bazy danych

Projekt wykorzystuje relacyjne modele ORM:

* 🧍 Kupujacy – Reprezentuje osoby lub podmioty odpowiedzialne za składanie zamówień. Każdy kupujący może mieć wiele zamówień.
* 🏢 Firma – Producent lub dostawca artykułów. Firma jest powiązana z artykułami, które oferuje.
* 🏬 Sklep – Miejsce zakupu (fizyczne lub online). Każde zamówienie jest przypisane do jednego sklepu.
* 🗂 Kategoria – Klasyfikacja artykułów według typu lub przeznaczenia (np. elektronika, narzędzia).
* 📦 Artykul\_Lista – Lista dostępnych produktów. Każdy artykuł jest powiązany z firmą i kategorią.
* 📄 Zamowienie – Reprezentuje pojedyncze zamówienie z datą, kupującym i sklepem.
* 🔗 lista\_dodanie – Tabela pośrednia realizująca relację wiele-do-wielu między Zamowieniem a Artykul\_Lista. Przechowuje ilość, cenę i rabaty.

---

## 💻 Wykorzystane biblioteki

Podstawowe:

* Python 3.x
* SQLAlchemy (ORM)
* SQLite (baza danych)
* tkinter (GUI)
* tkinterdnd2 (drag-and-drop)
* pygame (obsługa dźwięku)
* tkcalendar (kalendarz wyboru daty)
* Pillow / PhotoImage (ikony)
* TkToolTip (dodatkowe opisy dla przycisków)

---

## ⚙️ Instalacja i uruchomienie

1. Klonowanie repozytorium:

```bash
git clone https://github.com/MrEmsii/Torchik-Selling-Buying-Manager.git
cd Torchik-Selling-Buying-Manager
```

2. Instalacja zależności:
   Zalecane jest użycie virtualenv:

```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

Jeśli nie masz requirements.txt, zainstaluj ręcznie:

```bash
pip install sqlalchemy pygame tkcalendar tkinterdnd2
```

3. Uruchomienie programu:

```bash
python main.py
```

---

## 👤 Autor

Projekt stworzony przez:
🧑‍💻 Patryk Szczepanik (MrEmsii)

---

## 📄 Licencja

Projekt objęty licencją:
📘 CC BY-NC-ND 4.0 — Creative Commons Uznanie autorstwa – Użycie niekomercyjne – Bez utworów zależnych
Więcej informacji: [https://creativecommons.org/licenses/by-nc-nd/4.0/](https://creativecommons.org/licenses/by-nc-nd/4.0/)

Nie zezwala się na:

* użytek komercyjny,
* modyfikowanie kodu,
* tworzenie dzieł pochodnych.
