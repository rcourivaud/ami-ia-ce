/* eslint-disable import/namespace */
import React from 'react';
import { Button, Icon } from 'antd';
import PropTypes from 'prop-types';
import {Scrollbars} from 'react-custom-scrollbars';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import _ from 'lodash';
import { openNotificationWithIcon } from '../../../components/notification/index.jsx';
// Actions
import * as MeActions from '../../../core/redux/Me/actions.js';
import * as recordActions from '../../../core/redux/record/actions.js';
import * as RecordSelector from '../../../core/redux/record/selector.js';
import { handleSelectionPosition } from '../../../core/utils/selectedText';

class Category extends React.Component {
    /**
     * propTypes - define props
     * @desc define props required or not
     * @version 1.0
     * @since 1.0
     * @private
     */
    static propTypes = {
        toAnnot: PropTypes.number.isRequired,
        setCurrentLetter: PropTypes.func.isRequired,
        postAnnotationLabel: PropTypes.func.isRequired,
        setWrongOcr: PropTypes.func.isRequired,
        getRecordList: PropTypes.func.isRequired,
        currentLetter: PropTypes.object,
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
    };

    constructor(props) {
        super(props);
        this.state = {
            toAnnot: props.toAnnot,
            currentLetter: props.currentLetter,
        };
        this.handleValidation = this.handleValidation.bind(this);
        this.annotation = this.annotation.bind(this);
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'toAnnot',
            'currentLetter',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }
        return null;
    }

    handleValidation(statut) {
        const { toAnnot, currentLetter } = this.state;

        if (statut === false) {
            if (currentLetter) {
                const mutableLetter = currentLetter.toJS();
                this.props.setWrongOcr(mutableLetter.docId);
                return;
            }
        }
        this.props.setCurrentLetter(null);
        this.props.getRecordList(toAnnot === 0 ? 1 : 0);
    }

    annotation(key, concept) {
        const { currentLetter } = this.state;
        let termPosition = null;
        const selectedTerm = window.getSelection().toString();
        if (selectedTerm !== '') {
            const selection = window.getSelection();
            let node = selection.anchorNode;
            while (node.id !== 'annotation' && node.nodeName !== 'BODY'){
                node = node.parentNode;
            }
            if (node.id === 'annotation') {
                if ((termPosition = handleSelectionPosition(selectedTerm))) {
                    const selectedTermStart = termPosition.start;
                    const selectedTermEnd = termPosition.end;
                    if (selectedTermStart === -1 || selectedTermEnd === 1) {
                        openNotificationWithIcon('error', 'Erreur interne, votre annotation n\'a pas été sauvegarder');
                        return;
                    }
                    if (currentLetter) {
                        const tmp = currentLetter.toJS();
                        this.props.postAnnotationLabel(tmp.docId, selectedTerm,
                            tmp.name, key[0], selectedTermStart, selectedTermEnd);
                        openNotificationWithIcon('success', `l'expression '${this.trimmedTerm(selectedTerm)}' a été sauvegardé`);
                    }
                } else {
                    openNotificationWithIcon('error', 'Veuillez sélectionner un terme');
                    return;
                }
            } else {
                openNotificationWithIcon('error', 'Veuillez sélectionner dans la lettre');
                return;
            }
        } else {
            openNotificationWithIcon('error', 'Veuillez sélectionner un terme');
            return;
        }

    }

    trimmedTerm(str) {
        if (str.length > 300) {
            const trimmedString = str.substr(0, 300);
            return trimmedString.substr(0, Math.min(trimmedString.length, trimmedString.lastIndexOf(' '))) + '...';
        }
        else {
            return str;
        }
    }

    render() {
        const { currentLetter } = this.state;
        const disable = currentLetter ? false : true;

        return (
            <div style={ { padding: '0px'} }>
                <Button
                    type="primary"
                    style={ {margin: '5px',width: '98%'} }
                    onClick={ _.partial(this.handleValidation, true) }
                    disabled={ disable }
                >
                    <Icon type="check-circle" />
                    {'Terminer'}
                </Button>
                <Scrollbars
                    style={ { height: '83vh'} }
                >
                    <div style={ {align:'center',marginBottom:'13px'} }>
                        <h3>
                            <Icon type="bulb" theme="twoTone" style={ {marginRight: '2%'} } />
                            {'MOYEN'}
                        </h3>
                    </div>
                    <div>
                        <Button onClick={ _.partial(this.annotation, ['Moyen']) } disabled={ disable } size={ 'small' } style={ { width: '80%',marginBottom:'13px',fontSize:'11px',textAlign:'left', height:'35px' } }>
                            <h3>
                                <Icon type="down-square" theme="filled" style={ {fontSize:'14px', color:  '#fbc531', marginTop: '1%'} } />
                                { 'Moyens' }
                            </h3>
                        </Button>
                    </div>
                    <div style={ {align:'center',marginBottom:'13px'} }>
                        <h3>
                            <Icon type="setting" theme="twoTone" style={ {marginRight: '2%'} } />
                            {'CONCLUSION'}
                        </h3>
                    </div>
                    <div>
                        <Button onClick={ _.partial(this.annotation, ['Conclusion']) } disabled={ disable } size={ 'small' } style={ { width: '80%',marginBottom:'13px',fontSize:'11px',textAlign:'left', height:'35px' } }>
                            <h3>
                                <Icon type="down-square" theme="filled" style={ {fontSize:'14px', color: '#FF0000', marginTop: '1%'} } />
                                {'Conclusion' }
                            </h3>
                        </Button>
                    </div>
                    <div style={ {align:'center',marginBottom:'13px'} }>
                        <h3>
                            <Icon type="warning" theme="twoTone" style={ {marginRight: '2%'} } />
                            {'Un problème ?'}
                        </h3>
                    </div>
                    <Button onClick={ _.partial(this.handleValidation, false) } disabled={ disable } size={ 'small' } style={ { width: '80%',marginBottom:'13px',fontSize:'11px',textAlign:'left', height:'35px' } }>
                        <h3>
                            <Icon type="close-square" theme="filled" style={ {fontSize:'14px', color: '#FF0000', marginTop: '1%', marginRight: '1%'} } />
                            { 'Requête illisible' }
                        </h3>
                    </Button>
                </Scrollbars>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        toAnnot: RecordSelector.getToAnnot(state),
        currentLetter: RecordSelector.getCurrentLetter(state),
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
    return bindActionCreators({ ...MeActions, ...recordActions }, dispatch);
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Category));
