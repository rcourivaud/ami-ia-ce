select
content as "lettre",
statut_annotation as "status"
from test_requetes_meta_data
where request_id = ?
