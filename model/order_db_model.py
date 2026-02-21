from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime
import os

Base = declarative_base()


class ListaDodanie(Base):
    __tablename__ = "lista_dodanie"

    artykul_id = Column(Integer, ForeignKey("artykul_lista.id"), primary_key=True)
    zamowienie_id = Column(Integer, ForeignKey("zamowienie.id"), primary_key=True)

    ilosc_artykulu = Column(Integer, default=1)
    czas_druku_1_elem = Column(Float, default=0.0)
    waga_1_elem = Column(Float, default=0.0)
    koszt_1kg_materialu = Column(Float, default=0.0)
    cena_1_elem = Column(Float, default=0.0)

    artykul = relationship("Artykul_Lista", back_populates="pozycje")
    zamowienie = relationship("Zamowienie", back_populates="pozycje")


class Kupujacy(Base):
    __tablename__ = "kupujacy"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    zamowienia = relationship("Zamowienie", back_populates="kupujacy")


class Zamowienie(Base):
    __tablename__ = "zamowienie"

    id = Column(Integer, primary_key=True)
    realizacja_id = Column(Integer, default=0)
    data_zlozenia_zamowienia = Column(Date, default=datetime.date.today)
    data_deadline = Column(Date, nullable=True)
    data_wysylki = Column(Date, nullable=True)

    faktura_id = Column(Integer, ForeignKey("faktury.id"), nullable=True)
    kupujacy_id = Column(Integer, ForeignKey("kupujacy.id"))

    nazwa_zamowienia = Column(String, default="")
    opis_zamowienia = Column(String, default="")
    rabat_j = Column(Float, default=0.0)
    rabat_procent = Column(Float, default=0.0)

    kupujacy = relationship("Kupujacy", back_populates="zamowienia")
    faktura = relationship("Faktury", back_populates="zamowienie", uselist=False)

    pozycje = relationship(
        "ListaDodanie",
        back_populates="zamowienie",
        cascade="all, delete-orphan"
    )
    
    def oblicz_przychod(self):
        return sum(
            (p.ilosc_artykulu or 1) * (p.cena_1_elem or 0)
            for p in self.pozycje
        )

    def oblicz_koszta(self):
        return sum(
            (p.ilosc_artykulu or 1) * (p.waga_1_elem or 0) * (p.koszt_1kg_materialu or 0)
            for p in self.pozycje
        )

    def oblicz_dochod(self):
        rabat_proc = max((100 - self.rabat_procent) / 100, 0)
        return self.oblicz_przychod() * rabat_proc - self.rabat_j

    def oblicz_przychod_na_1h_druku(self):
        total_hours = sum((p.ilosc_artykulu or 1) * (p.czas_druku_1_elem or 0) for p in self.pozycje)
        return self.oblicz_przychod() / total_hours if total_hours > 0 else 0

    def oblicz_dochod_na_1h_druku(self):
        total_hours = sum((p.ilosc_artykulu or 1) * (p.czas_druku_1_elem or 0) for p in self.pozycje)
        return self.oblicz_dochod() / total_hours if total_hours > 0 else 0

class Faktury(Base):
    __tablename__ = "faktury"

    id = Column(Integer, primary_key=True)
    faktura_nr = Column(String)
    data_wystawienia = Column(Date, nullable=True)
    data_zaksiegowania_wplaty = Column(Date, nullable=True)

    zamowienie = relationship("Zamowienie", back_populates="faktura", uselist=False)


class Artykul_Lista(Base):
    __tablename__ = "artykul_lista"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    pozycje = relationship("ListaDodanie", back_populates="artykul")


def SQLconnect():
    db_path = os.path.join(os.path.dirname(__file__), "..", "database", "order_db.db")
    engine = create_engine(f"sqlite:///{db_path}")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()