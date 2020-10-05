import fs from 'fs-sync';
import path from 'path';

const queries = {
    //User
    // setUserLogStory: fs.read(path.join(__dirname, '/user/set-user-log-story.sql')),
    //Dashboard
    getMetrics: fs.read(path.join(__dirname, '/dashboard/get-metrics.sql')),
    getTa: fs.read(path.join(__dirname, '/dashboard/get-ta-stat.sql')),
    getMat: fs.read(path.join(__dirname, '/dashboard/get-mat-stat.sql')),

    // Record
    getRecordList: fs.read(path.join(__dirname, '/record/get-recordList.sql')),
    getRecord: fs.read(path.join(__dirname, './record/get-record.sql')),

    getListNoAnnot: fs.read(path.join(__dirname, '/record/get-list-no-anot.sql')),
    getListAnnot: fs.read(path.join(__dirname, '/record/get-list-user-anot.sql')),


    getAnnotation: fs.read(path.join(__dirname, './record/get-term-annote.sql')),

    deleteAnnotation: fs.read(path.join(__dirname, './record/delete-annotation.sql')),

    deleteOcr: fs.read(path.join(__dirname, './record/delete-ocr.sql')),


    setAnnotation: fs.read(path.join(__dirname, './record/set-annotation.sql')),

    setValidationRapport: fs.read(path.join(__dirname, './record/set-validation-rapport.sql')),
    //User
    setUserLogStory: fs.read(path.join(__dirname, './user/set-user-log.sql')),
};

export default {
    get: (queryName) => {
        return queries[queryName];
    },
};
