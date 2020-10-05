import { Map } from 'immutable';

/**
 * @constant state auth state
 * @public
 * @version 1.0
 * @since 1.0
 */
export default Map({
    isPending: false,
    error: null,
    recordList: null,
    toAnnot: 1,
    annotationList: null,
    currentLetter: null,
    letter: null,
});
