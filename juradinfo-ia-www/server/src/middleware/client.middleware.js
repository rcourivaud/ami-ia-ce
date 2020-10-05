import logger from '../tools/logger';
import adm from '@tools/adm.js';
import users from '@tools/user.js';
import _ from 'lodash';

function keyMiddleware(req, res, next) {
    if (req.headers && req.headers.key && req.headers.key === 'juradinfo-ia') {
        if (req.headers && req.headers['auth-user'] && req.headers['auth-user'].length > 0) {
            if (_.includes(users, req.headers['auth-user']) || _.includes(adm, req.headers['auth-user'])) {
                next();
            } else {
                logger.error(`forbidden acces ${req.headers['auth-user']} ${req.path}`);
                res.status(403).json({
                    error: 'redirect',
                });
            }
        } else {
            logger.error(`no DN ${req.method} ${req.path}`);
            res.status(404).json({
                error: 'DN is missing',
            });
        }
    } else {
        logger.error(`forbidden acces: ${req.method} ${req.path}`);
        res.status(403).json({
            error: 'forbidden access',
        });
    }
}

export { keyMiddleware };
