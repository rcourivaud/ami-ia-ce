const sorterString = (a,b) => {
    if (a > b) {
        return -1;
    }
    if (b > a) {
        return 1;
    }
    return 0;
};

const columnsMat = [
    {
        title: 'Matiere',
        dataIndex: 'matiere',
        key: 'matiere',
        width: '45%',
        sorter: (a, b) => sorterString(a.matiere, b.matiere),
    },
    {
        title: 'Total requête',
        dataIndex: 'nb_requetes_total',
        key: 'nb_requetes_total',
        width: '25%',
        sorter: (a, b) => a.nb_requetes_total - b.nb_requetes_total,
    },
    {
        title: 'Requête annotées',
        dataIndex: 'nb_requetes_annotees',
        key: 'address',
        width: '30%',
        sorter: (a, b) => a.nb_requetes_annotees - b.nb_requetes_annotees,
    },
];

export default columnsMat;
