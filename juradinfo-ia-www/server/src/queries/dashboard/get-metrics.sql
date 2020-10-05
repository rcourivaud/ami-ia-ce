SELECT
count(DISTINCT request_id) as 'total',
count(DISTINCT case when statut_annotation = 0 then request_id else null end) as 'missing'
from test_requetes_meta_data;
