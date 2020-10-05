import types from './constants.js';
import initialState from './state.js';

/**
 * @constant key normalize key
 * @desc key for normalizr and immutable
 * @version 1.0
 * @since 1.0
 * @public
 */
export const STATE_KEY = 'record';

/**
 * @function dataReducer redux reducer
 * @desc return new state according to the triggered action
 * @param {object} state redux state
 * @param {object} action action trigger
 * @return {object} state
 * @version 1.0
 * @since 1.0
 * @public
 */
export default function dataReducer(state = initialState, action) {
    switch (action.type) {
    case types.RECORD_PENDING:
    case types.DELETE_ANNOT_PENDING:
    case types.DELETE_OCR_PENDING:
    case types.PUSH_ANNOT_PENDING:
    case types.CURRENT_LETTER_PENDING:
    case types.CURRENT_LETTER_ANNOTATED_PENDING:
        return state.merge({
            error: null,
            isPending: true,
        });

    case types.CURRENT_LETTER_REJECTED:
    case types.CURRENT_LETTER_ANNOTATED_REJECTED:
        return state.merge({
            isPending: false,
            error: action.payload,
            letter: null,
            annotationList: null,
        });

    case types.DELETE_ANNOT_REJECTED:
    case types.DELETE_OCR_REJECTED:
    case types.PUSH_ANNOT_REJECTED:
        return state.merge({
            isPending: false,
            error: action.payload,
        });

    case types.DELETE_ANNOT_FULFILLED:
    case types.PUSH_ANNOT_FULFILLED:
        return state.merge({
            isPending: false,
            error: null,
            annotationList: action.payload.annotation,
        });

    case types.CURRENT_LETTER_FULFILLED:
        return state.merge({
            isPending: false,
            error: null,
            letter: action.payload.lettre,
        });

    case types.DELETE_OCR_FULFILLED:
        return state.merge({
            error: null,
            isPending: null,
            currentLetter: null,
        });

    case types.CURRENT_LETTER_ANNOTATED_FULFILLED:
        return state.merge({
            isPending: false,
            error: null,
            letter: action.payload.letter,
            annotationList: action.payload.annotation,
        });

    case types.RECORD_FULFILLED:
        return state.merge({
            isPending: false,
            error: null,
            recordList: action.payload,
            letter: null,
            currentLetter: null,
            annotationList: null,
        });

    case types.RECORD_REJECTED:
        return state.merge({
            isPending: false,
            error: action.payload,
            recordList: null,
        });

    case types.ADD_TO:
        return state.merge({
            isPending: false,
            error: null,
            toAnnot: action.payload.toAnnot,
        });

    case types.ADD_CURRENT_LETTER:
        return state.merge({
            isPending: false,
            error: null,
            recordList: null,
            currentLetter: action.payload.letter,
        });
    default:
        return state;
    }
}

