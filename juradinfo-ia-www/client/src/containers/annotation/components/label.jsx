/* eslint-disable react/jsx-no-bind */
import React from 'react';
import {  Icon, Table, Card, Tooltip, notification  } from 'antd';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import _ from 'lodash';
import {Scrollbars} from 'react-custom-scrollbars';
//Actions
import * as recordActions from '../../../core/redux/record/actions.js';
import * as RecordSelector from '../../../core/redux/record/selector.js';

const openNotificationWithIcon = (type, message, description) => {
    notification[type]({
        message,
        description,
        duration: 3,
    });
};

class Label extends React.Component {
    /**
     * propTypes - define props
     * @desc define props required or not
     * @version 1.0
     * @since 1.0
     * @private
     */
    static propTypes = {
        setToAnnot: PropTypes.func.isRequired,
        getRecordList: PropTypes.func.isRequired,
        deleteAnnotation: PropTypes.func.isRequired,
        toAnnot: PropTypes.number.isRequired,
        currentLetter: PropTypes.object,
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
        currentLetter: null,
        annotationList: null,
    };

    constructor(props) {
        super(props);
        this.state = {
            toAnnot: props.toAnnot,
            currentLetter: props.currentLetter,
            annotationList: props.annotationList,
        };
        this.deleteAnnotation = this.deleteAnnotation.bind(this);
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'toAnnot',
            'currentLetter',
            'annotationList',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }
        return null;
    }

    deleteAnnotation(text) {

        const data = {
            docId: text.request_id,
            username: text.username,
            selectedTerm: text.terms,
            startPos: text.startPos,
            endPos: text.endPos,
            categorie: text.categorie,
        };
        this.props.deleteAnnotation(data);
        openNotificationWithIcon('success', 'Annotation supprimée');
    }

    render() {
        const columns = [ {
            dataIndex: 'color',
            key: 'color',
            width: '1%',
            render:(text, row, index) =>{
                return  <Icon type="down-square" style={ { fontSize: '12px', color: '#1890FF' } } theme="filled" />;},
        },{
            title:
    <Tooltip title="Expression selectionné" placement="bottom">
        <Icon type="highlight" theme="twoTone" style={ { fontSize: '21px'} } />
    </Tooltip>
            ,
            dataIndex:'terms',
            key:
    <Tooltip title="Expression slectionné" placement="bottom">
        { 'terms'}
    </Tooltip>
            ,
            width: '40%',
            render:(text, row, index) =>{
                return  (
                    <Tooltip title={ text } placement="bottom">
                        {`${text.substr(0, 25)}...`}
                    </Tooltip>
                );},

        },{
            title:
    <Tooltip title="Catégorie" placement="bottom">
        <Icon type="tag" theme="twoTone" style={ { fontSize: '18px'} } />
    </Tooltip>
            ,
            dataIndex: 'categorie',
            key: 'categorie',
            width: '32%',
            render:(text, row, index) =>{
                return  (
                    <Tooltip title={ text } placement="bottom">
                        { text}
                    </Tooltip>
                );},
        },
        {
            title:
    <Tooltip title="Supprimer l'expression" placement="bottom">
        <Icon type="delete" theme="twoTone" style={ { fontSize: '19px'} } align="center" />
    </Tooltip>,
            dataIndex: 'code_supression',
            key: 'code_supression',
            width: '1%',
            render:(text, row, index) =>{
                return   (
                    <span>
                        <a>
                            <Icon type="close" style={ {fontSize: '19px',color:'#ff1001'} } onClick={ _.partial(this.deleteAnnotation, row) } />
                        </a>
                    </span>
                );},
        },

        ];

        const { annotationList } = this.state;
        return (
            <Card
                headStyle={ { textAlign: 'center' } }
                bodyStyle={ {  margin: '0px', padding: '0px'} }
            >
                <Scrollbars style={ { height: '83vh' } }>
                    {
                        <Table
                            rowKey={ record => record.code_supression }
                            dataSource={ annotationList ? annotationList.toJS() : [] }
                            columns={ columns }
                            pagination={ false }
                            size={ 'small' }
                        />
                    }
                </Scrollbars>
            </Card>
        );
    }
}

function mapStateToProps(state) {
    return {
        toAnnot: RecordSelector.getToAnnot(state),
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
    return bindActionCreators({ ...recordActions }, dispatch);
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Label));
