from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy import Table, Date, select
import datetime
import os, random
from dbControler import SQLconnect, select, Kupujacy, Kategoria, Sklep, Firma, Zamowienie, Artykul_Lista, artykuly_relacja


def Test(session):
    lista = []
    d = 100
    b = d*10
    g = d*100

    for i in range(0, d):
        kupujacy_1 = Kupujacy(nazwa="Firma"+str(i))
        sklep1 = Sklep(nazwa="Te2mu"+str(i))
        firma_1 = Firma(nazwa="Prusa4"+str(i))
        kategoria_1 = Kategoria(nazwa="maszyny"+str(i))
        art_1 = Artykul_Lista(nazwa="Azbest"+str(random.randint(1,g)), kategoria_id=random.randint(1, d), firma_id=random.randint(1, d))
        lista.extend((kupujacy_1, sklep1, firma_1, kategoria_1, art_1))

    for i in range(0, b):
        zamow_1 = Zamowienie(data=datetime.date(random.randint(2000,2026), random.randint(1, 12), random.randint(1, 28)),rabat_procent=random.randint(0, 50),rabat_j = random.randint(0, 1000), kupujacy_id = random.randint(1, d), sklep_id=random.randint(1, d))
        lista.append(zamow_1)
        
        
    session.add_all(lista)
    # session.add_all([kupujacy_1, firma_1, sklep1, kategoria_1, art_1, zamow_1])
    session.commit() # Ważne!

    for i in range(0, g):
        session.execute(artykuly_relacja.insert().values(
            zamowienie_id=random.randint(1, b),
            artykul_id=random.randint(1, d),
            cena_jednostkowa=random.randint(1, 1000),
            ilosc_artykulu = random.randint(1, 64)
        ))
        session.commit() # Ważne!

    print(f"Dodano artykuł {art_1.artykul} do zamówienia {zamow_1.id}")


if __name__ == "__main__":
    # Połączenie z bazą danych (przekaż odpowiednią ścieżkę)
    dsc = os.path.dirname(__file__) # lub inna ścieżka
    session = SQLconnect(dsc)

    Test(session) # Testowanie