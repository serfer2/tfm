import csv
import os
import traceback
import sys
from datetime import datetime
from typing import (
    List,
    Tuple,
)

from psycopg2 import connect

from application.services import (
    CategoryAnnotation,
    HackForumsThreadsExtraction,
)
from domain.models import Document
from infrastructure.repositories import (
    ForumDBRepository,
    ThreadSummaryDBRepository,
)
from shared.constants import (
    CAT_DEMAND,
    CAT_SUPPLY,
    RELATED_TERMS,
)

# usage:  python main.py [annotate | groundtruth]


def main():
    try:
        if 'annotate' in sys.argv:
            _generate_auto_annotated_datasets()
        elif 'groundtruth' in sys.argv:
            _generate_groundtruth_and_full_datasets()
        else:
            raise Exception('wrong option')
    except Exception:
        print(traceback.format_exc())
        print('usage: python entrypoint.py [annotate | groundtruth]')
        return 1
    return 0


def _generate_groundtruth_and_full_datasets() -> None:
    supply, demand = _load_category_annotated_datasets()
    documents = _extract_ddos_related_documents()
    ground_truth_documents = []

    _export_to_csv('datasets/ddos_full_dataset.csv', documents)

    for document in documents:

        document['category'] = ''
        if document['content'] in supply:
            document['category'] = CAT_SUPPLY
        elif document['content'] in demand:
            document['category'] = CAT_DEMAND

        if document['category']:
            ground_truth_documents.append(document)

    _export_to_csv(
        'datasets/ddos_ground_truth_dataset.csv',
        ground_truth_documents,
    )


def _load_category_annotated_datasets() -> Tuple[List[str]]:
    supply = []
    demand = []
    with open('supply.csv', 'r') as fin:
        for line in fin.readlines():
            _l = line.strip()
            if _l:
                supply.append(_l)
    with open('demand.csv', 'r') as fin:
        for line in fin.readlines():
            _l = line.strip()
            if _l:
                demand.append(_l)
    return supply, demand


def _generate_auto_annotated_datasets():
    """
        Generates trainning and test datasets by
        extracting DDoS related terms and splitting
        results (20% trainning, 80% test).
    """
    annotator = CategoryAnnotation()
    documents = _extract_ddos_related_documents()
    to_csv = [_annotate_document(annotator, doc) for doc in documents]
    _export_to_csv('datasets/ddos_auto_annotated_dataset.csv', to_csv)


def _annotate_document(annotator: CategoryAnnotation, doc: dict) -> dict:
    supply_terms = annotator.supply_terms(doc)
    demand_terms = annotator.demand_terms(doc)
    doc['supply'] = bool(supply_terms)
    doc['supply_terms'] = supply_terms
    doc['demand'] = bool(demand_terms)
    doc['demand_terms'] = demand_terms
    return {
        'content': doc['content'],
        'sell': doc['supply'],
        'supply_terms': ', '.join(doc['supply_terms']),
        'buy': doc['demand'],
        'demand_terms': ', '.join(doc['demand_terms']),
    }


def _export_to_csv(filepath: str, to_csv: List[dict]):
    with open(filepath, 'w', encoding='utf8', newline='') as fileout:
        csv_witer = csv.DictWriter(fileout, fieldnames=to_csv[0].keys())
        csv_witer.writeheader()
        csv_witer.writerows(to_csv)


def _extract_ddos_related_documents() -> List[Document]:
    dbc = connect(
        host=os.getenv('POSTGRES_HOST', 'localhost'),
        database=os.getenv('POSTGRES_DB', 'crimebb'),
        user=os.getenv('POSTGRES_USER', 'crimebb'),
        password=os.getenv('POSTGRES_PASSWORD', 'crimebbinlocalhost'),
    )

    data_extraction_service = HackForumsThreadsExtraction(
        forum_repository=ForumDBRepository(dbc=dbc),
        thread_summary_repository=ThreadSummaryDBRepository(dbc=dbc),
    )
    ddos_related_terms = RELATED_TERMS.get('tech_terms')

    start = datetime.now()
    print(f'*** Start ............. {start}')
    documents = data_extraction_service.extract(
        related_terms=ddos_related_terms,
    )
    end = datetime.now()
    print(f'*** Related threads ... {len(documents)}')
    print(f'*** End ............... {end}')

    return documents


if __name__ == '__main__':
    sys.exit(main())
