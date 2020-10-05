/* eslint-disable react/jsx-no-bind */
/* eslint-disable no-return-assign */
/* eslint-disable react/prop-types */
/* eslint-disable react/display-name */
import React from 'react';
import { Icon, Input, Button } from 'antd';

export default (params) => [
    {
        title: 'Requête',
        dataIndex: 'request_name',
        key: 'name',
        width: '46%',
        filterDropdown: ({
            setSelectedKeys, selectedKeys, confirm, clearFilters,
        }) => (
            <div className="custom-filter-dropdown">
                <Input
                    ref={ ele => params.searchInput = ele }
                    placeholder="Nom Lettre"
                    value={ selectedKeys[0] }
                    onChange={ e => setSelectedKeys(e.target.value ? [e.target.value] : []) }
                    onPressEnter={ params.handleSearch(selectedKeys, confirm) }
                />
                <Button type="primary" onClick={ params.handleSearch(selectedKeys, confirm) }>
                    {'Search'}
                </Button>
                <Button onClick={ params.handleReset(clearFilters) }>
                    {'Reset'}
                </Button>
            </div>
        ),
        filterIcon: filtered => <Icon type="search" style={ { color: filtered ? '#108ee9' : '#aaa' } } />,
        onFilter: (value, record) => record.request_name.toLowerCase().includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
                setTimeout(() => {
                    params.searchInput.focus();
                });
            }
        },
        render: text => {
            return text;
        },
    },

    {
        title: 'Matière',
        dataIndex: 'matiere',
        key: 'matiere',
        width: '33%',
        filterDropdown: ({
            setSelectedKeys, selectedKeys, confirm, clearFilters,
        }) => (
            <div className="custom-filter-dropdown">
                <Input
                    ref={ ele => params.searchInput = ele }
                    placeholder="Theme"
                    value={ selectedKeys[0] }
                    onChange={ e => setSelectedKeys(e.target.value ? [e.target.value] : []) }
                    onPressEnter={ params.handleSearch(selectedKeys, confirm) }
                />
                <Button type="primary" onClick={ params.handleSearch(selectedKeys, confirm) }>
                    {'Search'}
                </Button>
                <Button onClick={ params.handleReset(clearFilters) }>
                    {'Reset'}
                </Button>
            </div>
        ),
        filterIcon: filtered => <Icon type="search" style={ { color: filtered ? '#108ee9' : '#aaa' } } />,
        onFilter: (value, record) => record.matiere.toLowerCase().includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
                setTimeout(() => {
                    params.searchInput.focus();
                });
            }
        },
        render: text => {
            return text;
        },
    },

    {
        title: 'TA',
        dataIndex: 'ta',
        key: 'ta',
        width: '20%',
        filterDropdown: ({
            setSelectedKeys, selectedKeys, confirm, clearFilters,
        }) => (
            <div className="custom-filter-dropdown">
                <Input
                    ref={ ele => params.searchInput = ele }
                    placeholder="TA"
                    value={ selectedKeys[0] }
                    onChange={ e => setSelectedKeys(e.target.value ? [e.target.value] : []) }
                    onPressEnter={ params.handleSearch(selectedKeys, confirm) }
                />
                <Button type="primary" onClick={ params.handleSearch(selectedKeys, confirm) }>
                    {'Search'}
                </Button>
                <Button onClick={ params.handleReset(clearFilters) }>
                    {'Reset'}
                </Button>
            </div>
        ),
        filterIcon: filtered => <Icon type="search" style={ { color: filtered ? '#108ee9' : '#aaa' } } />,
        onFilter: (value, record) => record.ta.toLowerCase().includes(value.toLowerCase()),
        onFilterDropdownVisibleChange: (visible) => {
            if (visible) {
                setTimeout(() => {
                    params.searchInput.focus();
                });
            }
        },
        render: text => {
            return text;
        },
    },
];
