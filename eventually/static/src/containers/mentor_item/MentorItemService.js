const messagesListService = id => {
    let messages = null;

    if (id == 1) {
        messages = {
            'messages': [
                {
                    'id': 1,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                },
                {
                    'id': 2,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
                },
                {
                    'id': 3,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis.'
                },
                {
                    'id': 4,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 5,
                    'author': 'Me',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin.'
                },
                {
                    'id': 6,
                    'author': 'John Doe',
                    'avatar': 'johndoe',
                    'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse sollicitudin luctus enim ut sagittis. Proin varius lectus nulla, id dictum nisl ultricies eget. Donec vitae gravida justo, ut rhoncus felis. Maecenas mi urna, ornare sed rutrum eu, pulvinar sed lectus. Sed in odio lacinia, maximus arcu at, rhoncus nulla.'
                }
            ]
        };
    } 
    return messages;
};

const studentService = () => {
    let student = {
        'student':{
            'id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'avatar': 'johndoe'
        },

    };

    return student;
};

const itemInfoService = () => {

    let item_info = {
        'item_info':{
            'id': 1,
            'item_name': 'Python course',
            'text': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        },    
    };

    return item_info;
};

const answerInfoService = () => {

    let answer_info = {
        'answer_info':{
            'id': 1,
            'student_name': 'John Doe',
            'student_answer': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        },    
    };

    return answer_info;
};

export {messagesListService, studentService, itemInfoService, answerInfoService};
