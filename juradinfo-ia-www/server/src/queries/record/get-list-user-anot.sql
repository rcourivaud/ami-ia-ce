select
DISTINCT (req.request_id),
req.request_name,
req.matiere,
req.ta
from test_requetes_meta_data req
INNER join app_annotation annot on annot.username = ? and annot.request_id = req.request_id
where req.statut_annotation = 1 AND req.matiere IS NOT NULL and req.ta IS NOT NULL
