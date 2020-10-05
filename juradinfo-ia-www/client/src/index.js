/* eslint-disable react/jsx-filename-extension */
import 'react-app-polyfill/ie9';
import 'react-app-polyfill/stable';
import 'core-js/stable';
import React from 'react';
import ReactDOM from 'react-dom';
import './styles/index.css';
import { App } from './containers/App.jsx';
import * as serviceWorker from './serviceWorker';

if (navigator.userAgent.toLowerCase().indexOf('firefox') > -1){
    ReactDOM.render(<App />, document.getElementById('root'));
} else {
    document.getElementById('root').innerHTML = "<div><h1>Vous n'utilisez pas le bon navigateur web</h1><h3>Merci d'utiliser Mozilla Firefox</h3></div>";
}

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
