import axios from 'axios';

const appPath = '/api/v1/chat/';

const getReceiversList = (isMentor = false) => {

    let receivers = {};

    if (isMentor) {

        receivers = {
            'receivers': [
                {
                    'id': 10,
                    'first_name': 'Sam',
                    'last_name': 'Ruby',
                    'avatar': 'samruby',
                    'is_online': true
                },
                {
                    'id': 2,
                    'first_name': 'Marcelo',
                    'last_name': 'Petrov',
                    'avatar': 'marcelopetrov',
                    'is_online': false
                },
                {
                    'id': 9,
                    'first_name': 'Ismail',
                    'last_name': 'Botobo',
                    'avatar': 'ismailbotobo',
                    'is_online': true
                }
            ]
        };

    } else {

        receivers = {
            'receivers': [
                {
                    'id': 1,
                    'first_name': 'John',
                    'last_name': 'Doe',
                    'avatar': 'johndoe',
                    'is_online': true
                },
                {
                    'id': 2,
                    'first_name': 'Eric',
                    'last_name': 'Moreno',
                    'avatar': 'ericmoreno',
                    'is_online': false
                },
                {
                    'id': 3,
                    'first_name': 'Mark',
                    'last_name': 'Smith',
                    'avatar': 'marksmith',
                    'is_online': true
                }
            ]
        };
    }

    return receivers;
};

const getMessagesList = receiverId => {
    // const url = appPath + '1' + '/';
    // console.log(url);
    // let a = axios.get('/api/v1/chat/36/1/');
    // console.log(a);    
    return axios.get('/api/v1/chat/2/1/');
};

const postChatMessage = (receiverId, text) => {
    const postChatUrl = `${appPath}${receiverId}/`;
    return axios.post(postChatUrl, {
        'text': text
    });
};

export {getReceiversList, getMessagesList, postChatMessage};
