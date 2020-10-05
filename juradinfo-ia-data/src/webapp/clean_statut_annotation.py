#!/usr/bin/env python 
#-*- coding: utf-8 -*-

from sqlalchemy import create_engine
import datetime as dt

db_uri = "{dialecte}://{username}:{password}@{hostname}/{databasename}".format(
            dialecte="mysql+pymysql",
            username="to_be_set",
            password="to_be_set",
            hostname="to_be_set",
            databasename="to_be_set")
engine = create_engine(db_uri)


##########
# params #
db_app_requetes_tab = "test_requetes_meta_data"
db_app_annotation_tab = "app_annotation"
##############
# end params #
##############

with engine.connect() as con:
	con.execute("""
	UPDATE {} SET statut_annotation=0
	WHERE request_id not in (select request_id from {}) AND statut_annotation=1
	""".format(db_app_requetes_tab, db_app_annotation_tab))	

    con.execute("""
    UPDATE {} SET statut_annotation=1
    WHERE request_id IN (SELECT request_id FROM {}) AND statut_annotation=3
    """.format(db_app_requetes_tab, db_app_annotation_tab))

print(dt.datetime.now().strftime("%y-%m-%d %H:%M"))
print("Execution performed!")
