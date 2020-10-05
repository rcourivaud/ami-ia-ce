//Lib
import React from 'react';
import { Route,  withRouter , Redirect } from 'react-router';
import { connect } from 'react-redux';
import { bindActionCreators } from 'redux';
import  ConnectedSwitch  from './component/connected.jsx';
//Containers
import  Dashboard  from '../containers/dashboard/index.jsx';
import NavBar from '../containers/navbar/index.jsx';
//Selector
import * as MeActions from '../core/redux/Me/actions.js';
//Component
import { Layout } from 'antd';
import MainAnnotation from '../containers/annotation/index.jsx';

/**
 * RootRouter component
 * @class RootRouter
 * @reactProps {bool} isConnected - user is connected or not
 * @desc Entry point of the main router to dispatch route with reactRouter
 * @extends {React.Component}
 * @public
 * @version 1.0
 * @since 1.0
 */
class RootRouter extends React.Component {
    render() {
        return (
            <Layout style={ { minHeight: '100vh' } }>
                <NavBar />
                <ConnectedSwitch>
                    <Route exact path="/annotation" component={ MainAnnotation } />
                    <Route exact path="/statistique" component={ Dashboard } />
                    <Redirect from="/" to="/annotation" />
                </ConnectedSwitch>
            </Layout>
        );
    }
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
    return bindActionCreators({ ...MeActions }, dispatch);
}


export default withRouter(connect(null, mapDispatchToProps)(RootRouter));
