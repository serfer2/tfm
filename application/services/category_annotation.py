from typing import List

from shared.constants import RELATED_TERMS


class CategoryAnnotation:

    def __init__(self):
        self._currency_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_currency')
        self._supply_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_supply')
        self._demand_terms = RELATED_TERMS.get('trade_terms').get('trade_terms_demand')

    def supply_terms(self, doc: dict) -> List[str]:
        return self._matching_terms(self._supply_terms, doc)

    def demand_terms(self, doc: dict) -> List[str]:
        return self._matching_terms(self._demand_terms, doc)

    def _matching_terms(self, terms: List[str], doc: dict) -> List[str]:
        matching_terms = []
        words = self._doc_words(doc)
        for term in terms:
            if term in words:
                matching_terms.append(term)
        return matching_terms

    def _doc_words(self, doc: dict):
        return [w.strip() for w in doc.get('content').split(' ') if w.strip()]
