from sqlalchemy import (
    create_engine, Column, Integer, String,
    ForeignKey, Date, func, Index, Numeric
)
from sqlalchemy.orm import (
    sessionmaker, relationship,
    declarative_base
)

import datetime
import os

from decimal import Decimal

Base = declarative_base()


class ZamowienieArtykul(Base):
    __tablename__ = "lista_dodanie"

    zamowienie_id = Column(
        Integer,
        ForeignKey("zamowienie.id"),
        primary_key=True,
        index=True
    )

    artykul_id = Column(
        Integer,
        ForeignKey("artykul_lista.id"),
        primary_key=True,
        index=True
    )

    cena_jednostkowa = Column(Numeric(10, 2), default=0)
    ilosc_artykulu = Column(Integer, default=1)

    zamowienie = relationship("Zamowienie", back_populates="pozycje")
    artykul = relationship("Artykul_Lista")


Index(
    "ix_zamowienie_artykul",
    ZamowienieArtykul.zamowienie_id,
    ZamowienieArtykul.artykul_id
)

class Kupujacy(Base):
    __tablename__ = "kupujacy"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    zamowienia = relationship(
        "Zamowienie",
        back_populates="kupujacy",
        cascade="all, delete"
    )


class Kategoria(Base):
    __tablename__ = "kategoria"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    art_lista = relationship(
        "Artykul_Lista",
        back_populates="kategoria"
    )


class Sklep(Base):
    __tablename__ = "sklep"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    zamowienia = relationship(
        "Zamowienie",
        back_populates="sklep",
        cascade="all, delete"
    )


class Firma(Base):
    __tablename__ = "firma"

    id = Column(Integer, primary_key=True)
    nazwa = Column(String)

    art_lista = relationship(
        "Artykul_Lista",
        back_populates="firma"
    )


class Zamowienie(Base):
    __tablename__ = "zamowienie"

    id = Column(Integer, primary_key=True)
    data = Column(Date, default=datetime.date.today)
    faktura_id = Column(String, default=None)

    rabat_j = Column(Numeric(10, 2), default=0)
    rabat_procent = Column(Integer, default=0)

    kupujacy_id = Column(Integer, ForeignKey("kupujacy.id"), index=True)
    sklep_id = Column(Integer, ForeignKey("sklep.id"), index=True)

    kupujacy = relationship("Kupujacy", back_populates="zamowienia")
    sklep = relationship("Sklep", back_populates="zamowienia")

    # RELACJA DO POZYCJI
    pozycje = relationship(
        "ZamowienieArtykul",
        back_populates="zamowienie",
        cascade="all, delete-orphan",
        lazy="selectin"  # zapobiega N+1
    )

    # =================================================
    # METODY BIZNESOWE (wydajne)
    # =================================================

    def oblicz_cene(self):
        return sum(
            p.cena_jednostkowa * p.ilosc_artykulu
            for p in self.pozycje
        )

    def oblicz_cene_rabat(self):
        # rabat w procentach jako Decimal
        rabat_proc = Decimal('1') - Decimal(str(self.rabat_procent)) / Decimal('100') if self.rabat_procent else Decimal('1')
        
        return self.oblicz_cene() * rabat_proc - Decimal(self.rabat_j or 0)

    def get_ilosc_artykul(self, artykul_id: int):
        for p in self.pozycje:
            if p.artykul_id == artykul_id:
                return p.ilosc_artykulu
        return 0


class Artykul_Lista(Base):
    __tablename__ = "artykul_lista"

    id = Column(Integer, primary_key=True)
    kategoria_id = Column(Integer, ForeignKey("kategoria.id"), index=True)
    firma_id = Column(Integer, ForeignKey("firma.id"), index=True)

    nazwa = Column(String)
    kolor = Column(String, default=None)
    szczegoly = Column(String, default=None)

    kategoria = relationship("Kategoria", back_populates="art_lista")
    firma = relationship("Firma", back_populates="art_lista")


# =====================================================
# POŁĄCZENIE Z BAZĄ
# =====================================================

def SQLconnect():
    db_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "database",
        "stock_db.db"
    )

    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=False,
        pool_pre_ping=True,
        connect_args={"check_same_thread": False}
    )

    Base.metadata.create_all(engine)

    Session = sessionmaker(
        bind=engine,
        autoflush=False,
        expire_on_commit=False
    )

    return Session()