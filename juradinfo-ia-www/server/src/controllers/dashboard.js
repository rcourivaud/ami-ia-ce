import express from 'express';
import logger from '@tools/logger';
import DBManager from '@db-manager/index.js';

class DashController {
    constructor() {
        this.path = '/dashboard';
        this.router = express.Router();
        this.initializeRoutes = this.initializeRoutes.bind(this);
        this.getDashboard = this.getDashboard.bind(this);
        this.initializeRoutes();
    }

    initializeRoutes() {
        this.router.get(this.path, this.getDashboard);
    }

    getDashboard(req, res) {
        logger.info('Fetching statistique');
        DBManager.getStatByScope().then((stat) => {
            DBManager.getStatByTa().then((ta) => {
                DBManager.getStatByMatiere().then((mat) => {
                    logger.info('Successfully fetched statistique');
                    res.status(200).json({
                        stat: stat[0],
                        ta: ta,
                        mat: mat,
                    });
                }, (err) => {
                    res.status(504).json({
                        error: 'cannot get statistique',
                    });
                    logger.error('get mat: ' + err);
                });
            }, (err) => {
                res.status(504).json({
                    error: 'cannot get statistique',
                });
                logger.error('get ta: ' + err);
            });
        }, (err) => {
            res.status(504).json({
                error: 'cannot get statistique',
            });
            logger.error('get stat: ' + err);
        });
    }
}

export { DashController };
