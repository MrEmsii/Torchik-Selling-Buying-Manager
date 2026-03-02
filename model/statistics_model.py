from sqlalchemy import select, func
from model.stock_db_model import (
    Zamowienie, ZamowienieArtykul, Artykul_Lista,
    Kupujacy, Sklep, Firma, Kategoria
)


class StatisticsStockModel:
    def __init__(self, session):
        self.session = session

    # ============================================================
    # 1. STATYSTYKA: koszt artykułów z uwzględnieniem rabatów
    # ============================================================

    def koszt_artykulow(self):
        # 1. Suma brutto zamówienia + rabaty (max zamiast sum!)
        order_totals = (
            select(
                ZamowienieArtykul.zamowienie_id.label("zam_id"),
                func.sum(
                    ZamowienieArtykul.cena_jednostkowa *
                    ZamowienieArtykul.ilosc_artykulu
                ).label("order_brutto"),
                func.max(Zamowienie.rabat_j).label("rabat_j"),
                func.max(Zamowienie.rabat_procent).label("rabat_proc")
            )
            .join(Zamowienie, Zamowienie.id == ZamowienieArtykul.zamowienie_id)
            .group_by(ZamowienieArtykul.zamowienie_id)
            .subquery()
        )

        # 2. Wyrażenia kosztowe
        part_brutto = (
            ZamowienieArtykul.cena_jednostkowa *
            ZamowienieArtykul.ilosc_artykulu
        )

        rabat_kwotowy = (
            part_brutto
            / func.nullif(order_totals.c.order_brutto, 0)
            * func.coalesce(order_totals.c.rabat_j, 0)
        )

        rabat_proc_mnoznik = (
            1 - (func.coalesce(order_totals.c.rabat_proc, 0) / 100)
        )

        koszt_expr = (part_brutto - rabat_kwotowy) * rabat_proc_mnoznik

        # 3. Koszt pozycji
        article_costs = (
            select(
                ZamowienieArtykul.artykul_id.label("art_id"),
                koszt_expr.label("koszt")
            )
            .join(order_totals, order_totals.c.zam_id == ZamowienieArtykul.zamowienie_id)
            .subquery()
        )

        # 4. Sumowanie kosztów po artykule (grupowanie po nazwie!)
        stmt = (
            select(
                Artykul_Lista.nazwa.label("nazwa"),
                func.sum(article_costs.c.koszt).label("total_cost")
            )
            .join(article_costs, article_costs.c.art_id == Artykul_Lista.id)
            .group_by(Artykul_Lista.nazwa)   # ← KLUCZOWA POPRAWKA
            .order_by(func.sum(article_costs.c.koszt).desc())
        )

        return self.session.execute(stmt).all()

    # ============================================================
    # 2. STATYSTYKA: koszt wg firm
    # ============================================================

    def koszt_w_firma(self):
        firm_total = (
            select(
                Artykul_Lista.firma_id.label("firma_id"),
                func.sum(
                    ZamowienieArtykul.cena_jednostkowa *
                    ZamowienieArtykul.ilosc_artykulu
                ).label("firm_brutto")
            )
            .join(Artykul_Lista, Artykul_Lista.id == ZamowienieArtykul.artykul_id)
            .group_by(Artykul_Lista.firma_id)
            .subquery()
        )

        stmt = (
            select(
                Firma.nazwa,
                func.sum(firm_total.c.firm_brutto).label("total_cost")
            )
            .join(firm_total, firm_total.c.firma_id == Firma.id)
            .group_by(Firma.nazwa)
            .order_by(func.sum(firm_total.c.firm_brutto).desc())
        )

        return self.session.execute(stmt).all()

    # ============================================================
    # 3. STATYSTYKA: koszt wg sklepów
    # ============================================================

    def koszt_w_sklepach(self):
        sklep_total = (
            select(
                Zamowienie.sklep_id.label("sklep_id"),
                func.sum(
                    ZamowienieArtykul.cena_jednostkowa *
                    ZamowienieArtykul.ilosc_artykulu
                ).label("sklep_brutto")
            )
            .join(Zamowienie, Zamowienie.id == ZamowienieArtykul.zamowienie_id)
            .group_by(Zamowienie.sklep_id)
            .subquery()
        )

        stmt = (
            select(
                Sklep.nazwa,
                func.sum(sklep_total.c.sklep_brutto).label("total_cost")
            )
            .join(sklep_total, sklep_total.c.sklep_id == Sklep.id)
            .group_by(Sklep.nazwa)
            .order_by(func.sum(sklep_total.c.sklep_brutto).desc())
        )

        return self.session.execute(stmt).all()

    # ============================================================
    # 4. STATYSTYKA: koszt wg kupujących
    # ============================================================

    def koszt_w_kupujacych(self):
        kupujacy_total = (
            select(
                Zamowienie.kupujacy_id.label("kupujacy_id"),
                func.sum(
                    ZamowienieArtykul.cena_jednostkowa *
                    ZamowienieArtykul.ilosc_artykulu
                ).label("kup_brutto")
            )
            .join(Zamowienie, Zamowienie.id == ZamowienieArtykul.zamowienie_id)
            .group_by(Zamowienie.kupujacy_id)
            .subquery()
        )

        stmt = (
            select(
                Kupujacy.nazwa,
                func.sum(kupujacy_total.c.kup_brutto).label("total_cost")
            )
            .join(kupujacy_total, kupujacy_total.c.kupujacy_id == Kupujacy.id)
            .group_by(Kupujacy.nazwa)
            .order_by(func.sum(kupujacy_total.c.kup_brutto).desc())
        )

        return self.session.execute(stmt).all()

    # ============================================================
    # 5. STATYSTYKA: koszt wg kategorii
    # ============================================================

    def koszt_w_kategori(self):
        category_total = (
            select(
                Artykul_Lista.kategoria_id.label("kategoria_id"),
                func.sum(
                    ZamowienieArtykul.cena_jednostkowa *
                    ZamowienieArtykul.ilosc_artykulu
                ).label("cat_brutto")
            )
            .join(Artykul_Lista, Artykul_Lista.id == ZamowienieArtykul.artykul_id)
            .group_by(Artykul_Lista.kategoria_id)
            .subquery()
        )

        stmt = (
            select(
                Kategoria.nazwa,
                func.sum(category_total.c.cat_brutto).label("total_cost")
            )
            .join(category_total, category_total.c.kategoria_id == Kategoria.id)
            .group_by(Kategoria.nazwa)
            .order_by(func.sum(category_total.c.cat_brutto).desc())
        )

        return self.session.execute(stmt).all()
