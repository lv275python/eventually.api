const getCurriculums = () => {

    const curriculums = [
        {
            'id': 1,
            'name': 'Essentials of Modern WebUI',
            'description': 'Package Managers, Task Runners, CSS Preprocessors, Unit Testing WebUI, Module Bundlers, ES 2015.',
            'goals': ['Be a Senior dev'],
            'team': 1,
            'mentors': [46, 12],
            'created': 1511386400,
            'updated': 1511394690
        },
        {
            'id': 2,
            'name': 'Network Fundamentals',
            'description': 'This course will be interesting to people who want to learn something new or\
                            systematize/organize the existing knowledge about networks. Those could be the\
                            people who just start learning or those who already have some experience in using\
                            and configuring the network devices. The course is aimed at the QAs, as well as the\
                            developers. I am sure that you will get not only the theoretical knowledge, but based\
                            on the real examples of working with network commands and utilities, you will learn how\
                            to use them effectively in your work.',
            'goals': ['Be a Junior dev'],
            'team': 1,
            'mentors': [46],
            'created': 1511386400,
            'updated': 1511394690
        },
        {
            'id': 3,
            'name': 'Requirements',
            'description': 'Requirements in software development process. Sources of Requirements. Requirement\
                            engineering. Requirements in SCRUM. It contains the base knowledge of software requirements,\
                            its types and formats, the process of gathering, analyzing and documenting of requirements.',
            'goals': ['Be a Senior dev'],
            'team': 1,
            'mentors': [46, 12],
            'created': 1511386400,
            'updated': 1511394690
        }, {
            'id': 4,
            'name': 'Task estimation',
            'description': 'Introduction on Estimation and realization estimation process in developtement and testing.\
                            It contains basic principles of Estimation, main techniques of estimation and some examples\
                            which demonstrate how right to report work and time tracking options.',
            'goals': ['Be a Senior dev'],
            'team': 1,
            'mentors': [46, 12],
            'created': 1511386400,
            'updated': 1511394690
        },
    ];
    return curriculums;
};

const getTopicListService = curriculumId => {
    const id = curriculumId;
    const topics = {
        'topics': [
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
                'author':  23,
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
        ]
        
    };
    const result = [];
    topics.topics.forEach(element => {
        if (element.curriculum == curriculumId) {
            result.push(element);
        }
        
    });
    return result;
};


export { getCurriculums, getTopicListService };
