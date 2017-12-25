const getMentorStudentsList = () => {

    return [
        {
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'avatar': 'johndoe'
        },
        {
            'id': 2,
            'first_name': 'Eric',
            'last_name': 'Moreno',
            'avatar': 'ericmoreno'
        },
        {
            'id': 3,
            'first_name': 'Mark',
            'last_name': 'Smith',
            'avatar': 'marksmith'
        }
    ];
};

const getAllStudentsList = () => {

    return [
        {
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'avatar': 'johndoe'
        },
        {
            'id': 2,
            'first_name': 'Eric',
            'last_name': 'Moreno',
            'avatar': 'ericmoreno'
        },
        {
            'id': 3,
            'first_name': 'Mark',
            'last_name': 'Smith',
            'avatar': 'marksmith'
        },
        {
            'id': 4,
            'first_name': 'Jacob',
            'last_name': 'Anderson',
            'avatar': 'jacobanderson'
        },
        {
            'id': 5,
            'first_name': 'Matthew',
            'last_name': 'Bellamy',
            'avatar': 'matthewbellamy'
        },
        {
            'id': 6,
            'first_name': 'Jared',
            'last_name': 'Leto',
            'avatar': 'jaredleto'
        },
        {
            'id': 7,
            'first_name': 'Kurt',
            'last_name': 'Cobain',
            'avatar': 'kurtcobain'
        }
    ];
};

const getAvailableStudentsList = () => {

    return [
        {
            'id': 5,
            'first_name': 'Matthew',
            'last_name': 'Bellamy',
            'avatar': 'matthewbellamy'
        },
        {
            'id': 6,
            'first_name': 'Jared',
            'last_name': 'Leto',
            'avatar': 'jaredleto'
        },
        {
            'id': 7,
            'first_name': 'Kurt',
            'last_name': 'Cobain',
            'avatar': 'kurtcobain'
        }
    ];
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

export { getMentorStudentsList, getAllStudentsList, getAvailableStudentsList, getCurriculumTopics};
