const topicListService = () => {

    const topics = {
        'topics': [
            {
                'id': 4,
                'title': 'Python',
                'author': 12,
                'curriculum': 2,
                'description': 'Python basic course',
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
                'forcurriculum': 4,
                'description': 'Some description for HTML and CSS topic',
                'created_at': 1509539867,
                'updated_at': 1509539867,
            }
        ]
    };

    return topics;
};

const assignmentsListService = () => {

    const assignments = {
        'assignments': [
            {
                'id': 1,
                'title': 'Read some book'
            },
            {
                'id': 2,
                'title': 'Quiz'
            },
            {
                'id': 3,
                'title': 'Make homework'
            },
            {
                'id': 4,
                'title': 'Watch the video'
            },

        ]
    };

    return assignments;
};
export {topicListService, assignmentsListService};
