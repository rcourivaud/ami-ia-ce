import types from './constants.js';
import initialState from './state.js';

/**
 * @constant key normalize key
 * @desc key for normalizr and immutable
 * @version 1.0
 * @since 1.0
 * @public
 */
export const STATE_KEY = 'me';

/*
 * types.LOGOUT_FULILLED is handled in the reducers to reset all state
 */
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
    case types.ME_PENDING:
        return state.merge({
            error: null,
            isPending: true,
        });

    case types.ME_FULFILLED:
        return state.merge({
            isPending: false,
            doc_done: action.payload.username,
        });

    case types.ME_REJECTED:
        return state.merge({
            isPending: false,
            error: action.payload,
        });

    default:
        return state;
    }
}
