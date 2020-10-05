import { STATE_KEY as USER_ME_STATE_KEY } from './reducer';

/**
 * @function getName
 * @desc Get all normalized users
 * @returns {object} immutable object
 * @param {object} state
 * @version 1.0
 * @since 1.0
 * @public
 */
export const getName = ({ [USER_ME_STATE_KEY]: me  }) => me.get('username');

/**
 * @function getIsPending
 * @desc Get request status
 * @returns {object} immutable object
 * @param {object} state
 * @version 1.0
 * @since 1.0
 * @public
 */
export const getIsPending = ({ [USER_ME_STATE_KEY]: me }) => me.get('isPending');

/**
 * @function getError
 * @description Get request error
 * @returns {boolean}
 * @param {object} state
 * @version 1.0
 * @since 1.0
 * @public
 */
export const getError = ({ [USER_ME_STATE_KEY]: me }) => me.get('error');
