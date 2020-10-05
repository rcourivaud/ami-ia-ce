select distinct selectedTerm as "terms",
categorie as "categorie",
request_id,
username,
startPos,
endPos,
CONCAT(selectedTerm, request_id, username, categorie) as "code_supression"
from app_annotation
where request_id = ?
