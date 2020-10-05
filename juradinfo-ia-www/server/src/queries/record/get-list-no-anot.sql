select
request_name,
matiere,
ta,
request_id
from test_requetes_meta_data
where statut_annotation = 0 AND matiere IS NOT NULL and ta IS NOT NULL
GROUP BY RAND()*(2000-1)+10
LIMIT 5
