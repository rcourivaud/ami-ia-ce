// Lib
import Network from '../network.js';

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function getRecordList(statut) {
    return Network().get('/record/list', {
        statut,
    });
}

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function getCurrentLetter(docId, name) {
    return Network().get('/record/letter', {
        docId,
        name,
    });
}

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function getCurrentLetterAnnotation(docId, name) {
    return Network().get('/record/letter-annotation', {
        docId,
        name,
    });
}

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function deleteAnnotation(data) {
    return Network().post('/record/delete-annotation', {
        ...data,
    });
}

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function postWrongOcr(data) {
    return Network().post('/record/delete-ocr', {
        request_id: data,
    });
}

/**
 * @function getDashboard
 * @desc Make a GET request to get current user
 * @param {string} accessToken - userToken
 * @returns {promise} Network promise with the response
 * @version 1.0
 * @since 1.0
 * @public
 */
export function postAnnotation(data) {
    return Network().post('/record/post-annotation', {
        ...data,
    });
}
