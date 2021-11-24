import os
from datetime import datetime

from psycopg2 import connect

from application.services import HackForumsThreadsExtraction
from infrastructure.repositories import (
    ForumDBRepository,
    ThreadSummaryDBRepository,
)
from shared.constants import RELATED_TERMS

dbc = connect(
    host=os.getenv('POSTGRES_HOST', 'optional: set here PG DB Name'),
    database=os.getenv('POSTGRES_DB', 'optional: set here PG DB Name'),
    user=os.getenv('POSTGRES_USER', 'optional: set here PG DB User'),
    password=os.getenv('POSTGRES_PASSWORD', 'optional: set here PG DB Password'),
)

data_extraction_service = HackForumsThreadsExtraction(
    forum_repository=ForumDBRepository(dbc=dbc),
    thread_summary_repository=ThreadSummaryDBRepository(dbc=dbc),
)
ddos_related_terms = RELATED_TERMS.get('tech_terms')

start = datetime.now()
related_threads_data = data_extraction_service.extract(
    related_terms=ddos_related_terms,
)
end = datetime.now()

for related_thread_data in related_threads_data:
    print(
        f'[{related_thread_data.get("tstamp").strftime("%Y-%m-%d %H:%M:%S")}] '
        f'{related_thread_data.get("matching_terms")} -> '
        f'{related_thread_data.get("content")[:150]}'
    )

print(f'*** Start ............. {start}')
print(f'*** Related threads ... {len(related_threads_data)}')
print(f'*** End ............... {end}')
