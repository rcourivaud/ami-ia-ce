/* eslint-disable camelcase */
import express from 'express';
import DBManager from '@db-manager/index.js';
import logger from '@tools/logger';
import url from 'url';
import queryString from 'query-string';
import _ from 'lodash';

const adm = [
    'vjunique',
    'dmoreau',
    'jdcombrexelle',
    'tcharpentier',
    'ccostarramone',
    'gdambricourt',
    'jassu-ondo',
    'vsiyou-fotso',
];

class RecordController {
    constructor() {
        this.path = '/record';
        this.router = express.Router();
        this.initializeRoutes = this.initializeRoutes.bind(this);
        this.getRecordList = this.getRecordList.bind(this);
        this.getLetter = this.getLetter.bind(this);
        this.getLetterAnnotation = this.getLetterAnnotation.bind(this);
        this.deleteLetterAnnotation = this.deleteLetterAnnotation.bind(this);
        this.postLetterAnnotation = this.postLetterAnnotation.bind(this);

        this.initializeRoutes();
    }

    initializeRoutes() {
        this.router.get(`${this.path}/list`, this.getRecordList);
        this.router.get(`${this.path}/letter`, this.getLetter);
        this.router.get(`${this.path}/letter-annotation`, this.getLetterAnnotation);
        this.router.post(`${this.path}/delete-annotation`, this.deleteLetterAnnotation);
        this.router.post(`${this.path}/post-annotation`, this.postLetterAnnotation);
        this.router.post(`${this.path}/delete-ocr`, this.deleteOcr);
    }

    deleteOcr(req, res) {
        const { request_id } = req.body;
        logger.info(`loading delete ocr ${request_id}`);

        if ( request_id )  {
            DBManager.deleteOcr(request_id).then(() => {
                logger.info(`Successfully deleting OCR  ${request_id}`);
                DBManager.setUserLogStory(req.headers['auth-user'], `delete ocr ${request_id}`).then((ret) => {
                    res.status(200).json({
                        success: true,
                    });
                }, (error) => {
                    logger.error("Erreur d'insert in delete ocr: " + error);
                    res.status(500).json({
                        error: 'cannot delete ocr',
                    });
                });
            }, (err) => {
                res.status(500).json({
                    error: 'cannot delete OCR',
                });
                logger.error('deleteOcr error :' + err);
            });
        } else {
            res.status(500).json({
                error: 'wrong params',
            });
            logger.error('wrong params post delete ocr');
        }
    }

    deleteLetterAnnotation(req, res) {
        const { docId, username, selectedTerm, startPos, endPos, categorie} = req.body;
        logger.info(`loading delete annotation  ${docId}, ${selectedTerm}`);

        if ( docId &&  username && selectedTerm && startPos && endPos && categorie )  {
            DBManager.deleteAnnotation(docId, username, selectedTerm, startPos, endPos, categorie).then(() => {
                logger.info(`Successfully deleting annotation  ${docId}, ${selectedTerm}`);
                logger.info(`Fetching annotation ${docId}`);
                DBManager.getAnnotation(docId).then((result) => {
                    logger.info(`Successfully Fetching annotation ${docId}`);
                    DBManager.setUserLogStory(req.headers['auth-user'], `delete annotation  ${docId}, ${selectedTerm}`).then((ret) => {
                        res.status(200).json({
                            annotation: result,
                        });
                    }, (error) => {
                        logger.error("Erreur d'insert in delete Annot: " + error);
                        res.status(500).json({
                            error: 'cannot get update log',
                        });
                    });
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get annotation',
                    });
                    logger.error('deleteAnnotation error :' + err);
                });
            }, (err) => {
                res.status(500).json({
                    error: 'cannot delete annotation',
                });
                logger.error('deleteAnnotation error :' + err);
            });
        } else {
            res.status(500).json({
                error: 'wrong params',
            });
            logger.error('wrong params delete annotation');
        }
    }

    postLetterAnnotation(req, res) {
        const {docId, nom_lettre, selectedTerm, categorie, selectedTermStart, selectedTermEnd } = req.body;
        logger.info(`loading post annotation  ${docId}, ${selectedTerm}`);

        if ( docId && nom_lettre && selectedTerm && categorie && selectedTermStart && selectedTermEnd)  {
            DBManager.setAnnotation(req.body, req.headers['auth-user']).then(() => {
                logger.info(`Successfully adding annotation  ${docId}, ${selectedTerm}, ${categorie}`);
                logger.info(`Fetching all annotation ${docId}`);
                DBManager.getAnnotation(docId).then((result) => {
                    logger.info(`Successfully Fetching annotation ${docId}`);
                    if (result.length === 1) {
                        DBManager.setValidationRapport(docId).then((tmp) => {
                            logger.info(`Successfully adding true to letter ${docId}`);
                        }, (err) => {
                            logger.error('setValidationRapport error :' + err);
                        });
                    }
                    DBManager.setUserLogStory(req.headers['auth-user'], `Successfully adding annotation  ${docId}, ${selectedTerm}, ${categorie}`).then((ret) => {
                        res.status(200).json({
                            annotation: result,
                        });
                    }, (error) => {
                        logger.error("Erreur d'insert in post annotation: " + error);
                        res.status(500).json({
                            error: 'cannot update log in postAnnotation',
                        });
                    });
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get annotation',
                    });
                    logger.error('postAnnotation error :' + err);
                });
            }, (err) => {
                res.status(500).json({
                    error: 'cannot set annotation',
                });
                logger.error('postAnnotation error :' + err);
            });
        } else {
            res.status(500).json({
                error: 'wrong params',
            });
            logger.error('wrong params post annotation');
        }
    }

    getLetter(req, res) {
        logger.info('Fetching letter');
        const parsedUrl = url.parse(req.url);
        const params = queryString.parse(parsedUrl.query);

        logger.info(`Fetching letter without annot${params.docId}`);
        if (params.docId && params.name) {
            DBManager.getRecord(params.docId).then((result) => {
                logger.info(`Successfully Fetching letter ${params.docId}`);
                res.status(200).json(result);
            }, (err) => {
                res.status(500).json({
                    error: 'cannot get letter',
                });
                logger.error('getLetter error :' + err);
            });
        } else {
            res.status(500).json({
                error: 'wrong params',
            });
            logger.error('wrong params get letter');
        }
    }

    getLetterAnnotation(req, res) {
        logger.info('Fetching letter with annotation');
        const parsedUrl = url.parse(req.url);
        const params = queryString.parse(parsedUrl.query);

        if (params.docId && params.name) {
            DBManager.getRecord(params.docId).then((result) => {
                logger.info(`Successfully Fetching letter with annot${params.docId}`);
                DBManager.getAnnotation(params.docId).then((result2) => {
                    logger.info(`Successfully Fetching annotation ${params.docId}`);
                    res.status(200).json({
                        annotation: result2,
                        letter: result.lettre,
                    });
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get annotation',
                    });
                    logger.error('getLetterAnnot error :' + err);
                });
            }, (err) => {
                res.status(500).json({
                    error: 'cannot get letter',
                });
                logger.error('getLetterAnnot error :' + err);
            });
        } else {
            res.status(500).json({
                error: 'wrong params',
            });
            logger.error('wrong params get letter Annotation');
        }
    }


    /**
 * Record list controller
 * @class recordController
 * @desc this function returns the list of request depending if they are already annotated or not
 * @params status (1 = annotated, 0 not)
 * @public
 * @version 1.0
 * @since 1.0
 */
    getRecordList(req, res) {
        const parsedUrl = url.parse(req.url);
        const params = queryString.parse(parsedUrl.query);
        const dn = req.headers['auth-user'];

        if (_.includes(adm, dn)) {
            if (params.statut) {
                logger.info('Fetching Record list');
                DBManager.getRecordList(params).then((result) => {
                    logger.info('Successfully Fetching RECORD');
                    res.status(200).json(result);
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get list record',
                    });
                    logger.error('getRecordList error :' + err);
                });
            } else {
                res.status(500).json({
                    error: 'wrong params',
                });
                logger.error('wrong params record List');
            }
        } else {
            if (params.statut && params.statut === '0') {
                logger.info('Fetching Record list');
                DBManager.getListNotAnnotated().then((result) => {
                    logger.info('Successfully Fetching RECORD');
                    res.status(200).json(result);
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get list record',
                    });
                    logger.error('getRecordList error :' + err);
                });
            } else if (params.statut && params.statut === '1') {
                DBManager.getListAnnotated(dn).then((result) => {
                    logger.info('Successfully Fetching RECORD');
                    res.status(200).json(result);
                }, (err) => {
                    res.status(500).json({
                        error: 'cannot get list record',
                    });
                    logger.error('getRecordList error :' + err);
                });
            }
            else {
                res.status(500).json({
                    error: 'wrong params',
                });
                logger.error('wrong params record List');
            }
        }
    }
}

export { RecordController };
