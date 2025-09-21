from sqlalchemy import func, select
from model.db_model import artykuly_relacja, Artykul_Lista, Firma, Kategoria, Zamowienie, Sklep, Kupujacy

class StatisticsModel:
    def __init__(self, session):
        self.session = session

    def koszt_artykulow(self):
        """
        Koszt artykułów (uwzględnia rabaty procentowe i proporcjonalnie rabat kwotowy).
        """
        order_total = (
            select(
                artykuly_relacja.c.zamowienie_id.label("zamowienie_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("order_brutto")
            )
            .group_by(artykuly_relacja.c.zamowienie_id)
            .subquery()
        )

        article_total = (
            select(
                Zamowienie.id.label("zamowienie_id"),
                Artykul_Lista.id.label("artykul_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("art_brutto")
            )
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .join(Artykul_Lista, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Zamowienie.id, Artykul_Lista.id)
            .subquery()
        )

        stmt = (
            select(
                Artykul_Lista.nazwa,
                func.sum(
                    (
                        article_total.c.art_brutto
                        - (article_total.c.art_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                    )
                    * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
                ).label("total_cost")
            )
            .join(article_total, article_total.c.artykul_id == Artykul_Lista.id)
            .join(order_total, order_total.c.zamowienie_id == article_total.c.zamowienie_id)
            .join(Zamowienie, Zamowienie.id == article_total.c.zamowienie_id)
            .group_by(Artykul_Lista.nazwa)
            .order_by(func.sum(
                (
                    article_total.c.art_brutto
                    - (article_total.c.art_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                )
                * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
            ).desc())
        )
        return self.session.execute(stmt).all()

    def koszt_w_firma(self):
        """
        Koszt w firmach (uwzględnia rabaty proporcjonalnie).
        """
        order_total = (
            select(
                artykuly_relacja.c.zamowienie_id.label("zamowienie_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("order_brutto")
            )
            .group_by(artykuly_relacja.c.zamowienie_id)
            .subquery()
        )

        firm_total = (
            select(
                Zamowienie.id.label("zamowienie_id"),
                Artykul_Lista.firma_id.label("firma_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("firm_brutto")
            )
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .join(Artykul_Lista, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Zamowienie.id, Artykul_Lista.firma_id)
            .subquery()
        )

        stmt = (
            select(
                Firma.nazwa,
                func.sum(
                    (
                        firm_total.c.firm_brutto
                        - (firm_total.c.firm_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                    )
                    * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
                ).label("total_cost")
            )
            .join(firm_total, firm_total.c.firma_id == Firma.id)
            .join(order_total, order_total.c.zamowienie_id == firm_total.c.zamowienie_id)
            .join(Zamowienie, Zamowienie.id == firm_total.c.zamowienie_id)
            .group_by(Firma.id)
            .order_by(func.sum(
                (
                    firm_total.c.firm_brutto
                    - (firm_total.c.firm_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                )
                * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
            ).desc())
        )
        return self.session.execute(stmt).all()

    def koszt_w_sklepach(self):
        """
        Koszt w sklepach (uwzględnia rabaty proporcjonalnie).
        """
        order_total = (
            select(
                artykuly_relacja.c.zamowienie_id.label("zamowienie_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("order_brutto")
            )
            .group_by(artykuly_relacja.c.zamowienie_id)
            .subquery()
        )

        sklep_total = (
            select(
                Zamowienie.id.label("zamowienie_id"),
                Zamowienie.sklep_id.label("sklep_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("sklep_brutto")
            )
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .group_by(Zamowienie.id, Zamowienie.sklep_id)
            .subquery()
        )

        stmt = (
            select(
                Sklep.nazwa,
                func.sum(
                    (
                        sklep_total.c.sklep_brutto
                        - (sklep_total.c.sklep_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                    )
                    * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
                ).label("total_cost")
            )
            .join(sklep_total, sklep_total.c.sklep_id == Sklep.id)
            .join(order_total, order_total.c.zamowienie_id == sklep_total.c.zamowienie_id)
            .join(Zamowienie, Zamowienie.id == sklep_total.c.zamowienie_id)
            .group_by(Sklep.id)
            .order_by(func.sum(
                (
                    sklep_total.c.sklep_brutto
                    - (sklep_total.c.sklep_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                )
                * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
            ).desc())
        )
        return self.session.execute(stmt).all()

    def koszt_w_kupujacych(self):
        """
        Koszt w kupujących (uwzględnia rabaty proporcjonalnie).
        """
        order_total = (
            select(
                artykuly_relacja.c.zamowienie_id.label("zamowienie_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("order_brutto")
            )
            .group_by(artykuly_relacja.c.zamowienie_id)
            .subquery()
        )

        kupujacy_total = (
            select(
                Zamowienie.id.label("zamowienie_id"),
                Zamowienie.kupujacy_id.label("kupujacy_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("kup_brutto")
            )
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .group_by(Zamowienie.id, Zamowienie.kupujacy_id)
            .subquery()
        )

        stmt = (
            select(
                Kupujacy.nazwa,
                func.sum(
                    (
                        kupujacy_total.c.kup_brutto
                        - (kupujacy_total.c.kup_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                    )
                    * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
                ).label("total_cost")
            )
            .join(kupujacy_total, kupujacy_total.c.kupujacy_id == Kupujacy.id)
            .join(order_total, order_total.c.zamowienie_id == kupujacy_total.c.zamowienie_id)
            .join(Zamowienie, Zamowienie.id == kupujacy_total.c.zamowienie_id)
            .group_by(Kupujacy.id)
            .order_by(func.sum(
                (
                    kupujacy_total.c.kup_brutto
                    - (kupujacy_total.c.kup_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                )
                * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
            ).desc())
        )
        return self.session.execute(stmt).all()

    def koszt_w_kategori(self):
        """
        Koszt w kategoriach (uwzględnia rabaty procentowe i proporcjonalnie rabat kwotowy).
        """
        order_total = (
            select(
                artykuly_relacja.c.zamowienie_id.label("zamowienie_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("order_brutto")
            )
            .group_by(artykuly_relacja.c.zamowienie_id)
            .subquery()
        )

        category_total = (
            select(
                Zamowienie.id.label("zamowienie_id"),
                Artykul_Lista.kategoria_id.label("kategoria_id"),
                func.sum(artykuly_relacja.c.cena_jednostkowa * artykuly_relacja.c.ilosc_artykulu).label("cat_brutto")
            )
            .join(artykuly_relacja, Zamowienie.id == artykuly_relacja.c.zamowienie_id)
            .join(Artykul_Lista, Artykul_Lista.id == artykuly_relacja.c.artykul_id)
            .group_by(Zamowienie.id, Artykul_Lista.kategoria_id)
            .subquery()
        )

        stmt = (
            select(
                Kategoria.nazwa,
                func.sum(
                    (
                        category_total.c.cat_brutto
                        - (category_total.c.cat_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                    )
                    * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))  # rabat procentowy
                ).label("total_cost")
            )
            .join(category_total, category_total.c.kategoria_id == Kategoria.id)
            .join(order_total, order_total.c.zamowienie_id == category_total.c.zamowienie_id)
            .join(Zamowienie, Zamowienie.id == category_total.c.zamowienie_id)
            .group_by(Kategoria.id)
            .order_by(func.sum(
                (
                    category_total.c.cat_brutto
                    - (category_total.c.cat_brutto / order_total.c.order_brutto) * func.coalesce(Zamowienie.rabat_j, 0)
                )
                * (1 - (func.coalesce(Zamowienie.rabat_procent, 0) / 100.0))
            ).desc())
        )

        return self.session.execute(stmt).all()
