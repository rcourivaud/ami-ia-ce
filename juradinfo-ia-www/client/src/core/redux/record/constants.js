/**
 * @constant
 * @desc every action type
 * @version 1.0
 * @since 1.0
 * @public
 */
export default {
    RECORD: 'RECORD::RECORD',
    RECORD_PENDING: 'RECORD::RECORD_PENDING',
    RECORD_FULFILLED: 'RECORD::RECORD_FULFILLED',
    RECORD_REJECTED: 'RECORD::RECORD_REJECTED',

    ADD_TO: 'RECORD::ADD_TO',

    ADD_CURRENT_LETTER: 'RECORD::ADD_CURRENT_LETTER',

    CLEAR_ERROR: 'RECORD:CLEAR_ERROR',

    DELETE_OCR: 'RECORD::DELETE_OCR',
    DELETE_OCR_PENDING: 'RECORD::DELETE_OCR_PENDING',
    DELETE_OCR_FULFILLED: 'RECORD::DELETE_OCR_FULFILLED',
    DELETE_OCR_REJECTED: 'RECORD::DELETE_OCR_REJECTED',

    DELETE_ANNOT: 'RECORD::DELETE_ANNOT',
    DELETE_ANNOT_PENDING: 'RECORD::DELETE_ANNOT_PENDING',
    DELETE_ANNOT_FULFILLED: 'RECORD::DELETE_ANNOT_FULFILLED',
    DELETE_ANNOT_REJECTED: 'RECORD::DELETE_ANNOT_REJECTED',

    PUSH_ANNOT: 'RECORD::PUSH_ANNOT',
    PUSH_ANNOT_PENDING: 'RECORD::PUSH_ANNOT_PENDING',
    PUSH_ANNOT_FULFILLED: 'RECORD::PUSH_ANNOT_FULFILLED',
    PUSH_ANNOT_REJECTED: 'RECORD::PUSH_ANNOT_REJECTED',

    CURRENT_LETTER: 'RECORD::CURRENT_LETTER',
    CURRENT_LETTER_FULFILLED: 'RECORD::CURRENT_LETTER_FULFILLED',
    CURRENT_LETTER_PENDING: 'RECORD::CURRENT_LETTER_PENDING',
    CURRENT_LETTER_REJECTED: 'RECORD::CURRENT_LETTER_REJECTED',

    CURRENT_LETTER_ANNOTATED: 'RECORD::CURRENT_LETTER_ANNOTATED',
    CURRENT_LETTER_ANNOTATED_FULFILLED: 'RECORD::CURRENT_LETTER_ANNOTATED_FULFILLED',
    CURRENT_LETTER_ANNOTATED_PENDING: 'RECORD::CURRENT_LETTER_ANNOTATED_PENDING',
    CURRENT_LETTER_ANNOTATED_REJECTED: 'RECORD::CURRENT_LETTER_ANNOTATED_REJECTED',
};