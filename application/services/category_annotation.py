from typing import List

from shared.constants import RELATED_TERMS


class CategoryAnnotation:

    def __init__(self):
        self._currency_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_currency')
        self._supply_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_supply')
        self._demand_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_demand')

    def auto_annotate(self, doc: dict) -> None:
        """
        Annotates category to a document by applying:
        - Supply: Doc has some currency term and supply term.
        - Demand: Doc has some currency term and demand term.
        - Other: any other case.
        """
        pass

    def is_supply(self, doc: dict) -> bool:
        return (
            self._has_currency(doc) and
            self._any_term_in_words(self._supply_terms, doc)
        )

    def is_demand(self, doc: dict) -> bool:
        return (
            self._has_currency(doc) and
            self._any_term_in_words(self._demand_terms, doc)
        )

    def supply_terms(self, doc: dict) -> List[str]:
        return self._matching_terms(self._supply_terms, doc)

    def demand_terms(self, doc: dict) -> List[str]:
        return self._matching_terms(self._demand_terms, doc)

    def _has_currency(self, doc: dict) -> bool:
        return self._any_term_in_words(self._currency_terms, doc)

    def _any_term_in_words(self, terms: List[str], doc: dict) -> bool:
        words = self._doc_words(doc)
        for term in terms:
            if term in words:
                return True
        return False

    def _matching_terms(self, terms: List[str], doc: dict) -> List[str]:
        matching_terms = []
        words = self._doc_words(doc)
        for term in terms:
            if term in words:
                matching_terms.append(term)
        return matching_terms

    def _doc_words(self, doc: dict):
        return [w.strip() for w in doc.get('content').split(' ') if w.strip()]
