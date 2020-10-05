select
request_name,
matiere,
ta,
request_id
from test_requetes_meta_data
where statut_annotation = ? AND matiere IS NOT NULL and ta IS NOT NULL
