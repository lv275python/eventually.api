import axios from 'axios';

const appPath = '/api/v1/mentor/students/';

const getStudentsList = (chosenTopic, isTopicDone, fromDate, toDate) => {
    // console.log(chosenTopic, isTopicDone, fromDate, toDate);
    const getStudentsUrl = `${appPath}?topic=${chosenTopic}&is_done=${isTopicDone}&from=${fromDate}&to=${toDate}/`;
    return axios.get(getStudentsUrl);
};

const postStudentList = (studentId, chosenTopic) => {
    const postStudentsUrl = `${appPath}`;
    return axios.post(postStudentsUrl, {
        'student': studentId,
        'topic': chosenTopic
    });
};

const getCurriculumTopics = () => {
    return [
        {
            'id': 4,
            'title': 'Node.js',
            'author': 12,
            'curriculum': 1,
            'description': 'Have you ever wanted to create a full-fledged web application, beyond just a simple\
            HTML page? In this course, you will learn how to set up a web server, interact with\
            a database and much more! This course will start off by teaching you the basics of\
            Node.js and its core modules. You will then learn how to import additional modules\
            and configure your project using npm. From there, you will learn how to use Express\
            to set up a web server and how to interact with a MongoDB database using Mongoose.\
            By the end of the course you will have created several real-world projects such\
            as a web scraper, a blogging API, and a database migration script.',
            'created_at': 1509539867,
            'updated_at': 1509539867,
        },
        {
            'id': 3,
            'title': 'JavaScript',
            'author': 23,
            'curriculum': 1,
            'description': 'This course for advanced knowladge',
            'created_at': 1509539867,
            'updated_at': 1509539867,
        },
        {
            'id': 2,
            'title': 'HTML/CSS',
            'author': 123,
            'curriculum': 1,
            'description': 'Some description for HTML and CSS topic',
            'created_at': 1509539867,
            'updated_at': 1509539867,
        }
    ];
};

export {getStudentsList, getCurriculumTopics, postStudentList};
