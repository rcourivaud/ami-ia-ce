/* eslint-disable camelcase */
import mysql from 'mysql2/promise';
import Queries from '@queries/index.js';
import logger from '@tools/logger.js';
import dotenv from 'dotenv';
import path from 'path';

function isDev() {
    return (process.env.NODE_ENV === 'development');
}

class DBManager {
    constructor() {
        dotenv.config({ path: path.resolve(__dirname, isDev ? '../../.env' : './env') });
        this.init();
    }
    //Init connection to datbase
    async init(){
        logger.debug('Initializing database connection');
        const url = process.env.HOST;
        const username = process.env.USER_DB;
        const pass = process.env.PASSWORD_DB;
        const dbName = process.env.DB_NAME;

        this.pool = await mysql.createPool({
            host     : url,
            user     : username,
            password : pass,
            database : dbName,
        });
        //        await this.pool.connect();
    }

    async runQuery(query, params) {
        const [rows] = await this.pool.query(query, params, async (err, row, fields) => {
            if (err) {
                throw err;
            }
        });
        return rows;
    }
    //Record
    async getRecordList(params) {
        const result = await this.runQuery(Queries.get('getRecordList'), params.statut);
        return result;
    }

    async getListNotAnnotated() {
        const result = await this.runQuery(Queries.get('getListNoAnnot'));
        return result;
    }

    async getListAnnotated(dn) {
        const result = await this.runQuery(Queries.get('getListAnnot'), dn);
        return result;
    }

    async getRecord(id) {
        const result = await this.runQuery(Queries.get('getRecord'), id);
        return result[0];
    }

    async getAnnotation(id) {
        const result = await this.runQuery(Queries.get('getAnnotation'), id);
        return result;
    }

    async deleteOcr(docId) {
        const result = await this.runQuery(Queries.get('deleteOcr'), [docId]);
        return result.rows;
    }

    async deleteAnnotation(docId, username, selectedTerm, startPos, endPos, categorie) {
        const result = await this.runQuery(Queries.get('deleteAnnotation'), [docId, selectedTerm, startPos, endPos, categorie]);
        return result.rows;
    }

    async setAnnotation({docId,nom_lettre,selectedTerm,categorie,selectedTermStart,selectedTermEnd}, user) {
        const result = await this.runQuery(Queries.get('setAnnotation'), [categorie, docId,nom_lettre,selectedTerm, selectedTermStart,selectedTermEnd, user]);
        return result;
    }

    async setValidationRapport( docId ) {
        const result = await this.runQuery(Queries.get('setValidationRapport'), docId);
        return result.rows;
    }

    //Dashboard
    async getStatByScope() {
        const ret = await this.runQuery(Queries.get('getMetrics'));
        return ret;
    }

    async getStatByTa() {
        const ret = await this.runQuery(Queries.get('getTa'));
        return ret;
    }

    async getStatByMatiere() {
        const ret = await this.runQuery(Queries.get('getMat'));
        return ret;
    }
    //User
    async setUserLogStory(user, message) {
        await this.runQuery(Queries.get('setUserLogStory'), [message, user]);
    }

}

export default new DBManager();
