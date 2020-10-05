SELECT t1.ta_code, t1.nb_requetes_total, IFNULL(t2.nb_requetes_annotees, 0) as nb_requetes_annotees
FROM (SELECT ta_code, count(*) as nb_requetes_total
FROM test_requetes_meta_data
GROUP BY ta_code) t1

LEFT JOIN

(SELECT ta_code, count(*) as nb_requetes_annotees
FROM test_requetes_meta_data
WHERE statut_annotation=1
GROUP BY ta_code) t2

ON t1.ta_code=t2.ta_code
ORDER BY nb_requetes_annotees DESC
