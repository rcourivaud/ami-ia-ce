/* eslint-disable react/jsx-max-depth */
import React, { Component } from 'react';
import { Layout, Row, Col, Spin, Card, Progress, Icon, Table } from 'antd';
import PropTypes from 'prop-types';
import _ from 'lodash';
import { withRouter } from 'react-router';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
//Selector
import * as DashSelector from '../../core/redux/dashboard/selector.js';
import * as DashActions from '../../core/redux/dashboard/actions.js';
import { openNotificationWithIcon } from '../../components/notification/index.jsx';
import columnsTa from './schema/ta.js';
import columnsMat from './schema/mat.js';

const { Content } = Layout;
const antIcon = <Icon type="loading" style={ { fontSize: 24 } } spin />;

class Dashboard extends Component {
    static propTypes = {
        isPending: PropTypes.bool.isRequired,
        error: PropTypes.object,
        getStat: PropTypes.func.isRequired,
        stat: PropTypes.object,

    };
    /**
     * defaultProps - define default value props
     * @desc define not required props
     * @private
     * @version 1.0
     * @since 1.0
     */
    static defaultProps = {
        stat: null,
        error: null,
    };

    constructor(props) {
        super(props);
        this.props.getStat();

        this.state = {
            error: props.error,
            isPending: props.isPending,
            stat: props.stat,
        };
        this.getPercent = this.getPercent.bind(this);
        this.calcRate = this.calcRate.bind(this);
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextProps.error) {
            openNotificationWithIcon('error', 'Erreur interne, veuillez notifier l\'administrateur du site');
        }
        return true;
    }
    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'isPending',
            'error',
            'stat',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }

        return null;
    }

    calcRate(nbKo, nbOk) {
        const ko = parseFloat(nbKo);
        const ok = parseFloat(nbOk);
        const sum = ko + ok;
        let ret = 100 * ok / sum;
        ret = ret.toFixed(2);
        return parseFloat(ret);
    }

    getPercent(percent) {
        if (percent === 100) {
            return 'Done';
        } else {
            return `${percent}%`;
        }
    }

    render() {
        const { isPending, stat } = this.state;
        let mutableStat = {};
        let mutableTa = [];
        let mutableMat = [];
        let percent = 0;
        let done = 0;
        let miss = 0;

        if (stat) {
            mutableStat = stat.toJS();
            mutableTa = mutableStat.ta;
            mutableMat = mutableStat.mat;
            mutableStat = mutableStat.stat;
            percent = this.calcRate(mutableStat.missing, (mutableStat.total - mutableStat.missing));
            done = mutableStat.total - mutableStat.missing;
            miss = mutableStat.missing;
        }
        console.log(mutableTa, mutableMat);

        return (
            <Content style={ { marginTop: '94px'} }>
                <Row>
                    <Spin spinning={ isPending } indicator={ antIcon }>
                        <Col xs={ { span: 5, offset: 1 } } lg={ { span: 6, offset: 1 } }>
                            <Card title={ 'Annotation total' } headStyle={ {textAlign: 'center', fontWeight:'bold'} }>
                                <b style={ {marginRight: '5%'} }>
                                    {`Annotées : ${done}`}
                                    <br />
                                    {`À annoter : ${miss}`}
                                </b>
                                <Progress
                                    type="dashboard"
                                    percent={  percent }
                                    format={ this.getPercent }
                                />
                            </Card>
                        </Col>
                        <Col xs={ { span: 5, offset: 1 } } lg={ { span: 6, offset: 1 } }>
                            <Card title={ 'Annotation total par TA' } headStyle={ {textAlign: 'center', fontWeight:'bold'} }>
                                <Table
                                    columns={ columnsTa } dataSource={ mutableTa }
                                />
                            </Card>
                        </Col>
                        <Col xs={ { span: 7, offset: 1 } } lg={ { span: 8, offset: 1 } }>
                            <Card title={ 'Annotation total par Matière' } headStyle={ {textAlign: 'center', fontWeight:'bold'} }>
                                <Table
                                    columns={ columnsMat } dataSource={ mutableMat }
                                />
                            </Card>
                        </Col>
                    </Spin>
                </Row>
            </Content>
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
        stat: DashSelector.getStat(state),
        isPending: DashSelector.getIsPending(state),
        error: DashSelector.getError(state),
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
        ...bindActionCreators({ ...DashActions}, dispatch),
    };
}


export default withRouter(connect(mapStateToProps, mapDispatchToProps)(Dashboard));
