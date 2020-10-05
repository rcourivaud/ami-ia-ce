SELECT IFNULL(t1.matiere, "Pas de matière") as matiere, t1.nb_requetes_total, IFNULL(t2.nb_requetes_annotees, 0) as nb_requetes_annotees
FROM (SELECT matiere, count(*) as nb_requetes_total
FROM test_requetes_meta_data
GROUP BY matiere) t1

LEFT JOIN

(SELECT matiere, count(*) as nb_requetes_annotees
FROM test_requetes_meta_data
WHERE statut_annotation=1
GROUP BY matiere) t2

ON t1.matiere=t2.matiere
