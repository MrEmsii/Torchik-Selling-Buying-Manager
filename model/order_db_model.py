from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table, Date, select
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
import datetime
import os

Base = declarative_base()

artykuly_relacja = Table(
    'lista_dodanie', Base.metadata,
    Column('artykul_id', Integer, ForeignKey('artykul_lista.id')),
    Column('zamowienie_id', Integer, ForeignKey('zamowienie.id')),
    Column("ilosc_artykulu", Integer, default=1),
    Column("czas_druku_1_elem", Integer, default=0),
    Column("waga_1_elem", Integer, default=0),
    Column("koszt_1kg_materialu", Integer, default=0),
    Column("cena_1_elem", Integer, default=0)
)


class Kupujacy(Base):
    __tablename__ = 'kupujacy'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    zamowienia = relationship('Zamowienie', back_populates='kupujacy')

class Zamowienie(Base):
    __tablename__ = 'zamowienie'
    id = Column(Integer, primary_key=True)
    realizacja_id = Column(Integer, default=0)
    data_zlozenia_zamowienia = Column(Date, default=datetime.date.today)
    data_deadline = Column(Date, nullable=True)
    data_wysylki = Column(Date, nullable=True)

    faktura_id = Column(Integer, ForeignKey("faktury.id"), nullable=True)
    kupujacy_id = Column(Integer, ForeignKey('kupujacy.id'))

    nazwa_zamowienia = Column(String, default="")
    rabat_j = Column(Integer, default=0)
    rabat_procent = Column(Integer, default=0)

    kupujacy = relationship('Kupujacy', back_populates='zamowienia')
    faktura = relationship('Faktury', back_populates='zamowienie', uselist=False)
    artykuly = relationship('Artykul_Lista', secondary=artykuly_relacja, back_populates='zamowienia')
    
    def oblicz_przychod(self, session):
        total = 0
        for artykul in self.artykuly:
            wynik = self._get_zamowienie_artykul_miejsce(artykul, session)
            if wynik is not None:
                ilosc = wynik[2] if wynik[2] is not None else 1 
                cena = wynik[6] if wynik[6] is not None else 0 
                total += ilosc * cena
        return total

    def oblicz_dochod(self, session):
        rabat_proc = max((100 - self.rabat_procent) / 100, 0)
        #dodać koszta!!!
        return self.oblicz_przychod(session) * rabat_proc - self.rabat_j
    
    def oblicz_koszta(self, session):
        total = 0
        for artykul in self.artykuly:
            wynik = self._get_zamowienie_artykul_miejsce(artykul, session)
            if wynik is not None:
                ilosc = wynik[2] if wynik[2] is not None else 1 
                koszt_1kg_materialu = wynik[5] if wynik[5] is not None else 0 
                waga_1_elem = wynik[4] if wynik[4] is not None else 0 
                total += ilosc * koszt_1kg_materialu * waga_1_elem
        return total

    def oblicz_przychod_na_1h_druku(self, session):
        total_hours = sum(self.get_ilosc_artykul(art, session) * (self._get_czas_druku(art, session) or 0)
                          for art in self.artykuly)
        #dodać koszta!!!
        return self.oblicz_przychod(session) / total_hours if total_hours > 0 else 0

    def oblicz_dochod_na_1h_druku(self, session):
        total_hours = sum(self.get_ilosc_artykul(art, session) * (self._get_czas_druku(art, session) or 0)
                          for art in self.artykuly)
        return self.oblicz_dochod(session) / total_hours if total_hours > 0 else 0

    def get_ilosc_artykul(self, artykul, session):
        wynik = self._get_zamowienie_artykul_miejsce(artykul, session)
        return wynik[2] if wynik is not None else 1

    def _get_czas_druku(self, artykul, session):
        wynik = self._get_zamowienie_artykul_miejsce(artykul, session)
        return wynik[3] if wynik is not None else 0

    def _get_zamowienie_artykul_miejsce(self, artykul, session):
        stmt = select(artykuly_relacja).where(
            artykuly_relacja.c.zamowienie_id == self.id,
            artykuly_relacja.c.artykul_id == artykul.id
        )
        return session.execute(stmt).fetchone()


class Faktury(Base):
    __tablename__ = 'faktury'
    id = Column(Integer, primary_key=True)
    faktura_nr = Column(String)
    data_wystawienia = Column(Date, nullable=True)
    data_zaksiegowania_wplaty = Column(Date, nullable=True)

    zamowienie = relationship('Zamowienie', back_populates='faktura', uselist=False)


class Artykul_Lista(Base):
    __tablename__ = 'artykul_lista'
    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    zamowienia = relationship('Zamowienie', secondary=artykuly_relacja, back_populates='artykuly')


def SQLconnect():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'order_db.db')
    engine = create_engine(f'sqlite:///{db_path}')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()
