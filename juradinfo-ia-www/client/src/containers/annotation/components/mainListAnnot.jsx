/* eslint-disable react/jsx-no-bind */
/* eslint-disable react/display-name */
/* eslint-disable import/namespace */
import React from 'react';
import { Table, Radio, Divider } from 'antd';
import PropTypes from 'prop-types';
import { connect } from 'react-redux';
import { withRouter } from 'react-router-dom';
import { bindActionCreators } from 'redux';
import getSchema from './table-schema.jsx';
import _ from 'lodash';
// Actions
import * as MeActions from '../../../core/redux/Me/actions.js';
import * as recordActions from '../../../core/redux/record/actions.js';
import * as RecordSelector from '../../../core/redux/record/selector.js';

class MainListAnnot extends React.Component {
    /**
     * propTypes - define props
     * @desc define props required or not
     * @version 1.0
     * @since 1.0
     * @private
     */
    static propTypes = {
        listLetter: PropTypes.array.isRequired,
        setToAnnot: PropTypes.func.isRequired,
        getRecordList: PropTypes.func.isRequired,
        toAnnot: PropTypes.number.isRequired,
        setCurrentLetter: PropTypes.func.isRequired,
        getLetter: PropTypes.func.isRequired,
    };

    constructor(props) {
        super(props);
        this.state = {
            listLetter: props.listLetter,
            toAnnot: props.toAnnot,
            searchText: '',
            tableSchema: getSchema(this),
        };
        this.handleChangeAnnotState = this.handleChangeAnnotState.bind(this);
        this.handleRowClick = this.handleRowClick.bind(this);
    }

    static getDerivedStateFromProps(nextProps, prevState) {
        const keys = [
            'listLetter',
            'toAnnot',
        ];

        const mutableProps = _.pick(nextProps, keys);
        const stateToCompare = _.pick(prevState, keys);

        if (!_.isEqual(mutableProps, stateToCompare)) {
            return mutableProps;
        }
        return null;
    }

    handleSearch = (selectedKeys, confirm) => () => {
        confirm();
        this.setState({ searchText: selectedKeys[0] });
    }

      handleReset = clearFilters => () => {
          clearFilters();
          this.setState({ searchText: '' });
      }

      handleChangeAnnotState(e) {
          if (e.target.value === 'Annot') {
              this.props.setToAnnot();
              this.props.getRecordList(1);
          }
          else {
              this.props.setToAnnot();
              this.props.getRecordList(0);
          }
      }

      handleRowClick(record) {
          const letter = {
              docId: record.request_id,
              name: record.request_name,
              matiere: record.matiere,
              ta: record.ta,
          };
          this.props.setCurrentLetter(letter);
          this.props.getLetter();
      }

      render() {
          const { listLetter, toAnnot, tableSchema } = this.state;

          return (
              <div style={ { minHeight: '80vh', marginTop: '2%' } }>
                  <Radio.Group onChange={ this.handleChangeAnnotState } value={ toAnnot === 1 ? 'toAnnot' : 'Annot' } buttonStyle="solid" style={ { marginBottom: '2%', marginLeft: '30%' } }>
                      <Radio.Button value="toAnnot">
                          {'Pas annotée'}
                      </Radio.Button>
                      <Divider type="vertical" style={ { backgroundColor: 'black' } } />
                      <Radio.Button value="Annot">
                          {'Déja annotée'}
                      </Radio.Button>
                  </Radio.Group>
                  <Table
                      size="small"
                      // eslint-disable-next-line react/jsx-no-bind
                      rowKey={ record => record.request_id }
                      style={ { backgroundColor: '#FFFFFF' } }
                      pagination={ { pageSize: 9 } }
                      dataSource={ listLetter }
                      columns={ tableSchema }
                      onRow={ (record, rowIndex) => {
                          return {
                              onClick: _.partial(this.handleRowClick, record),
                          };
                      } }
                  />
              </div>
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
    return bindActionCreators({ ...MeActions, ...recordActions }, dispatch);
}

export default withRouter(connect(mapStateToProps, mapDispatchToProps)(MainListAnnot));
