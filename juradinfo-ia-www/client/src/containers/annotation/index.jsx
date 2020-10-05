/* eslint-disable react/jsx-handler-names */
import React from 'react';
import PropTypes from 'prop-types';
import _ from 'lodash';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import { Layout, Icon, Spin, Col } from 'antd';
//Selector
import * as recordSelector from '../../core/redux/record/selector.js';
import * as recordActions from '../../core/redux/record/actions.js';
import Category from './components/category.jsx';
import Letter from './components/letter.jsx';
import MainListAnnot from './components/mainListAnnot.jsx';
import AnnotationLeft from './components/AnnotationLeft.jsx';
import { openNotificationWithIcon } from '../../components/notification/index.jsx';

const { Content } = Layout;
const antIcon = <Icon type="loading" style={ { fontSize: 24 } } spin />;

class MainAnnotation extends React.Component {
    static propTypes = {
        isPending: PropTypes.bool.isRequired,
        error: PropTypes.object,
        getRecordList: PropTypes.func.isRequired,
        recordList: PropTypes.object,
        currentLetter: PropTypes.object,
        letter: PropTypes.string,
        annotationList: PropTypes.object,
    };
    /**
     * defaultProps - define default value props
     * @desc define not required props
     * @private
     * @version 1.0
     * @since 1.0
     */
    static defaultProps = {
        recordList: null,
        error: null,
        currentLetter: null,
        letter: null,
        annotationList: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            error: props.error,
            isPending: props.isPending,
            recordList: props.recordList,
            currentLetter: props.currentLetter,
            letter: props.letter,
            annotationList: props.annotationList,
        };
        props.getRecordList(0);
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.error) {
            if (nextProps.error.data === 'redirect') {
                window.location.href = 'https://intranet.conseil-etat.fr/';
            } else {
                openNotificationWithIcon('error', 'Erreur interne, veuillez notifier l\'administrateur du site');
            }
        }
        return true;
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'isPending',
            'error',
            'recordList',
            'currentLetter',
            'letter',
            'annotationList',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }

        return null;
    }

    render() {
        const { isPending, recordList, currentLetter, letter,  annotationList } = this.state;
        let listLetter =  [];

        if (recordList) {
            listLetter = recordList.toJS();
        }

        return (
            <Layout>
                <Content style={ { marginTop: '64px', overflowX: 'hidden'} }>
                    <Spin spinning={ isPending } indicator={ antIcon }>
                        <Col span={ currentLetter ? 6 : 9 }>
                            {
                                currentLetter ?
                                    <AnnotationLeft currentLetter={ currentLetter } annotationList={ annotationList } />
                                    :
                                    <MainListAnnot listLetter={ listLetter } />
                            }
                        </Col>
                        <Col span={ currentLetter ? 12 : 9  }>
                            <Letter content={ letter } letter={ currentLetter } annotationList={ annotationList } />
                        </Col>
                        <Col span={ 6 }>
                            <Category />
                        </Col>
                    </Spin>
                </Content>
            </Layout>
        );
    }
}
/**
* @function mapStateToProps - redux method
* @desc transfert value state key into the props component
* @param {object} state - redux state
* @return {object} props
* @version 1.0
* @since 1.0
* @private
*/
function mapStateToProps(state) {
    return {
        recordList: recordSelector.getRecordList(state),
        isPending: recordSelector.getIsPending(state),
        error: recordSelector.getError(state),
        currentLetter: recordSelector.getCurrentLetter(state),
        letter: recordSelector.getLetter(state),
        annotationList: recordSelector.getAnnotationList(state),
    };
}

/**
 * @function mapDispatchToProps - redux method
 * @desc make action available in the props component.
 * @param {object} dispatch - redux-thunk dispatcher
 * @return {object} MeActions & AnonymousAddressActions
 * @version 1.0
 * @since 1.0
 * @private
 */
function mapDispatchToProps(dispatch) {
    return {
        dispatch,
        ...bindActionCreators({ ...recordActions}, dispatch),
    };
}


export default withRouter(connect(mapStateToProps, mapDispatchToProps)(MainAnnotation));
