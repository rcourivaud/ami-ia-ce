const sorterString = (a,b) => {
    if (a > b) {
        return -1;
    }
    if (b > a) {
        return 1;
    }
    return 0;
};


const columnsTa = [
    {
        title: 'TA',
        dataIndex: 'ta_code',
        key: 'ta_code',
        sorter: (a, b) => sorterString(a.ta_code, b.ta_code),
    },
    {
        title: 'Total requête',
        dataIndex: 'nb_requetes_total',
        key: 'nb_requetes_total',
        sorter: (a, b) => a.nb_requetes_total - b.nb_requetes_total,
    },
    {
        title: 'Requête annotées',
        dataIndex: 'nb_requetes_annotees',
        key: 'address',
        sorter: (a, b) => a.nb_requetes_annotees - b.nb_requetes_annotees,
    },
];

export default columnsTa;
