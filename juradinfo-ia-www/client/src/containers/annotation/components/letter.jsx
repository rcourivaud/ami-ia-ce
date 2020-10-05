/* eslint-disable camelcase */
/* eslint-disable react/jsx-no-bind */
/* eslint-disable react/display-name */
/* eslint-disable import/namespace */
import React from 'react';
import { Icon, Result, Table} from 'antd';
import PropTypes from 'prop-types';
import {Scrollbars} from 'react-custom-scrollbars';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import escapeStringRegexp from 'escape-string-regexp';
import _ from 'lodash';

function createMarkup(texte) {
    return {__html: texte};
}

const columns = [{
    title: 'Value',
    dataIndex: 'reponse',
    render: (text, row, index) => <div dangerouslySetInnerHTML={ createMarkup(text) } />,
}];

class Letter extends React.Component {
    /**
     * propTypes - define props
     * @desc define props required or not
     * @version 1.0
     * @since 1.0
     * @private
     */
    static propTypes = {
        letter: PropTypes.object,
        content: PropTypes.string,
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
        letter: null,
        annotationList: null,
        content: null,
    };


    constructor(props) {
        super(props);
        this.state = {
            letter: props.letter,
            content: props.content,
            annotationList: props.annotationList,
        };
        this.generateLetterHtml = this.generateLetterHtml.bind(this);
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'letter',
            'content',
            'annotationList',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }
        return null;
    }

    generateHtmlForAnnotation(text, annotatedTerms) {
        text = text.replace(/ +(?= )/g,'');
        _.forEach(annotatedTerms, item => {
            const titleToolTip =  `${item.categorie}`;
            const tmpText = item.terms.replace(/\r\n/g, '<br>');
            const finalText = escapeStringRegexp(tmpText);
            const termRegex = new RegExp(`(${finalText})(?=[^>]*<)`, 'gi');
            if (item.categorie === 'Moyen') {
                text = text.replace(termRegex, `<Tooltip title=${titleToolTip}><b style='font-weight:normal;background-color:#fbc531'>$1</b></Tooltip>`);
            } else {
                text = text.replace(termRegex, `<Tooltip title=${titleToolTip}><b style='font-weight:normal;background-color:red'>$1</b></Tooltip>`);
            }
        });
        return text;
    }

    generateLetterHtml(letter, terms) {
        const generateEOL = letter.replace(/###/g,'<br>');
        if (terms) {
            return [{
                reponse: this.generateHtmlForAnnotation(generateEOL, terms),
                id: 42,
            }];
        } else {
            return [{
                reponse: generateEOL,
                id: 42,
            }];
        }
    }



    render() {
        const { content, letter, annotationList } = this.state;
        if (letter) {
            const mutableLetter = letter.toJS();
            const lettreName = `${mutableLetter.name}`;
            let terms = [];
            if (annotationList) {
                terms = annotationList.toJS();
            }
            let htmlData = [];
            if (content) {
                htmlData = this.generateLetterHtml(content, terms);

            }
            return (
                <div style={ {backgroundColor: '#e6f5ff', minHeight: '80vh'} }>
                    <div style={ { backgroundColor: '#F0F2F5', textAlign:'center' ,padding:'10px'} }>
                        <Icon type="unordered-list" style={ { fontSize: '18px',paddingRight:'11px'} }  />
                        <b>
                            { lettreName }
                        </b>
                    </div>
                    <Scrollbars style={ { height: '83vh' } }>
                        <Table
                            id="annotation"
                            columns={ columns }
                            dataSource={ htmlData }
                            rowKey={ record => record.id }
                            bordered
                            pagination={ false }
                            showHeader={ false }
                            size="small"
                            style={ { backgroundColor: '#e6f5ff',fontSize: '0px'} }
                        />
                    </Scrollbars>
                </div>);

        } else {
            return (
                <div style={ {backgroundColor: '#e6f5ff', minHeight: '80vh'} }>
                    <Result
                        title="Veuillez sélectionner une requête à gauche"
                    />
                </div>
            );

        }
    }
}

export default withRouter(connect(null, null)(Letter));
