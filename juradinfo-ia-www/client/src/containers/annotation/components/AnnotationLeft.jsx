import React from 'react';
import { Layout, Card } from 'antd';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import _ from 'lodash';
import Label from './label.jsx';

const { Content } = Layout;

class AnnotationLeft extends React.Component {
    /**
     * propTypes - define props
     * @desc define props required or not
     * @version 1.0
     * @since 1.0
     * @private
     */
    static propTypes = {
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
            currentLetter: props.currentLetter,
            annotationList: props.annotationList,
        };
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
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

    render() {
        const { annotationList, currentLetter } = this.state;

        return (
            <div style={ { minHeight: '80vh', marginTop: '1%' } }>
                <Content style={ { marginTop: '0px' } }>
                    <Card
                        headStyle={ { textAlign: 'center' } }
                        bodyStyle={ {  margin: '0px', padding: '0px'} }
                        style={ { width: '100%' } }
                    >
                        <Label annotationList={ annotationList } currentLetter={ currentLetter } />
                    </Card>
                </Content>
            </div>
        );
    }
}

export default withRouter(connect(null, null)(AnnotationLeft));
