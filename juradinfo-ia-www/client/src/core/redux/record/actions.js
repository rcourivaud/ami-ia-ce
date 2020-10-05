/* eslint-disable camelcase */
import * as ErrorActions from '../Error/actions.js';
import types from './constants.js';
import * as MeSelector from '../Me/selector.js';
import * as RecordSelector from '../record/selector.js';
import { Map } from 'immutable';

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function getRecordList(statut) {
    return (dispatch, getState, { api }) => {

        return dispatch({
            type: types.RECORD,
            payload: api.getRecordList(statut),
        }).catch((err) => {
            ErrorActions.rejectPromiseWithLocalError(err.message);
        });
    };
}

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
*/
export function getLetter() {
    return (dispatch, getState, { api }) => {
        const state = getState();
        const toAnnot = RecordSelector.getToAnnot(state);
        const tpmLetter = RecordSelector.getCurrentLetter(state);
        const letter = tpmLetter.toJS();
        if (toAnnot) {
            return dispatch({
                type: types.CURRENT_LETTER,
                payload: api.getCurrentLetter(letter.docId, letter.name),
            }).catch((err) => {
                ErrorActions.rejectPromiseWithLocalError(err.message);
            });
        } else {
            return dispatch({
                type: types.CURRENT_LETTER_ANNOTATED,
                payload: api.getCurrentLetterAnnotation(letter.docId, letter.name),
            }).catch((err) => {
                ErrorActions.rejectPromiseWithLocalError(err.message);
            });
        }
    };
}

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function setToAnnot() {
    return (dispatch, getState, { api }) => {
        const state = getState();
        let toAnnot = RecordSelector.getToAnnot(state);
        if (toAnnot === 0) {
            toAnnot = 1;
        } else {
            toAnnot = 0;
        }
        return dispatch({
            type: types.ADD_TO,
            payload: { toAnnot },
        });
    };
}

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function deleteAnnotation(data) {
    return (dispatch, _, { api }) => {

        return dispatch({
            type: types.DELETE_ANNOT,
            payload: api.deleteAnnotation(data),
        }).catch((err) => {
            ErrorActions.rejectPromiseWithLocalError(err.message);
        });
    };
}
/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function setWrongOcr(request_id) {
    return (dispatch, getState, { api }) => {
        const state = getState();
        const toAnnot = RecordSelector.getToAnnot(state);
        return dispatch({
            type: types.DELETE_OCR,
            payload: api.postWrongOcr(request_id).then(() => dispatch({
                type: types.RECORD,
                payload: api.getRecordList(toAnnot === 0 ? 1 : 0),
            })).catch((err2) => {
                ErrorActions.rejectPromiseWithLocalError(err2.message);
            }),
        }).catch((err) => {
            ErrorActions.rejectPromiseWithLocalError(err.message);
        });
    };
}

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function postAnnotationLabel(docId, selectedTerm, nom_lettre, categorie, selectedTermStart, selectedTermEnd) {
    return (dispatch, getState, { api }) => {
        const state = getState();
        const name = MeSelector.getName(state) || Map({});
        const data = {
            docId, selectedTerm, nom_lettre,
            categorie,
            selectedTermStart, selectedTermEnd,
            user: name,
        };
        return dispatch({
            type: types.PUSH_ANNOT,
            payload: api.postAnnotation(data),
        }).catch((err) => {
            ErrorActions.rejectPromiseWithLocalError(err.message);
        });
    };
}

/**
 * @function getRecord
 * @desc This function send a get request to
 * get the letters statut and id.
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function setCurrentLetter(letter) {
    return (dispatch, _, { api }) => {

        return dispatch({
            type: types.ADD_CURRENT_LETTER,
            payload: { letter },
        });
    };
}

/**
 * @function clearError
 * @desc This function clear error object
 * @returns {object} the promise
 * @version 1.0
 * @since 1.0
 * @public
 */
export function clearError() {
    return (dispatch) => dispatch({
        type: types.CLEAR_ERROR,
    });
}

