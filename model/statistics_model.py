from sqlalchemy import func, select
from model.db_model import artykuly_relacja, Artykul_Lista, Firma, Kategoria, Zamowienie, Sklep, Kupujacy

class StatisticsModel:
    def __init__(self, session):
        self.session = session

    def koszt_artykulu(self):
        """
        Zwraca listę artykułów i ich całkowity koszt (suma cena_jednostkowa * ilość).
        """
        stmt = (
            select(
                Artykul_Lista.nazwa,
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(artykuly_relacja, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Artykul_Lista.id)
        )
        return self.session.execute(stmt).all()


    def srednia_cena_artykulu(self):
        """
        Średnia wartość artykułu (średnia cena jednostkowa).
        """
        stmt = (
            select(
                Artykul_Lista.nazwa,
                func.avg(artykuly_relacja.c.cena_jednostkowa).label("avg_price")
            )
            .join(artykuly_relacja, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Artykul_Lista.id)
            .order_by(func.avg(artykuly_relacja.c.cena_jednostkowa).desc())  # <-- sortowanie malejąco
            .order_by(func.count(Artykul_Lista.id).desc())

        )
        return self.session.execute(stmt).all()

    def koszt_w_kategori(self):
        """
        Kategoria, która wygenerowała największy koszt ogółem.
        """
        stmt = (
            select(
                Kategoria.nazwa,
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(Artykul_Lista, Artykul_Lista.kategoria_id == Kategoria.id)
            .join(artykuly_relacja, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Kategoria.id)
            .order_by(func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).desc())
            
        )
        return self.session.execute(stmt).all()

    def koszt_w_firma(self):
        """
        Firma, która wygenerowała największy koszt ogółem.
        """
        stmt = (
            select(
                Firma.nazwa,
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(Artykul_Lista, Artykul_Lista.firma_id == Firma.id)
            .join(artykuly_relacja, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Firma.id)
            .order_by(func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).desc())
            .order_by(func.count(Artykul_Lista.id).desc())
            
        )
        return self.session.execute(stmt).all()

    def koszt_w_sklepach(self):
        """
        Firma, która wygenerowała największy koszt ogółem.
        """
        stmt = (
            select(
                Sklep.nazwa,
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(Zamowienie, Zamowienie.sklep_id == Sklep.id)
            .join(Artykul_Lista, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .group_by(Sklep.id)
            .order_by(func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).desc())
            .order_by(func.count(Artykul_Lista.id).desc())
            
        )
        return self.session.execute(stmt).all()

    def koszt_w_kupujacych(self):
        """
        Firma, która wygenerowała największy koszt ogółem.
        """
        stmt = (
            select(
                Kupujacy.nazwa,
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(Zamowienie, Zamowienie.kupujacy_id == Kupujacy.id)
            .join(Artykul_Lista, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .group_by(Kupujacy.id)
            .order_by(func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).desc())
            .order_by(func.count(Artykul_Lista.id).desc())
            
        )
        return self.session.execute(stmt).all()

    def najpopularniejsza_kategoria(self):
        """
        Kategoria z największą liczbą artykułów i jej koszt.
        """
        stmt = (
            select(
                Kategoria.nazwa,
                func.count(Artykul_Lista.id).label("articles_count"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("total_cost")
            )
            .join(Artykul_Lista, Kategoria.id == Artykul_Lista.kategoria_id)
            .join(artykuly_relacja, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Kategoria.id)
            .order_by(func.count(Artykul_Lista.id).desc())
        )
        return self.session.execute(stmt).all()
