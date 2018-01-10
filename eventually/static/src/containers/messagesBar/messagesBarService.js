import axios from 'axios';

const appPath = '/api/v1/chat/';

const getReceiversList = (isMentor = false) => {

    let receivers = {};

    if (isMentor) {

        receivers = {
            'receivers': [
                {
                    'id': 36,
                    'first_name': 'Sam',
                    'last_name': 'Ruby',
                    'avatar': 'samruby',
                    'is_online': false
                },
                {
                    'id': 1,
                    'first_name': 'Marcelo',
                    'last_name': 'Petrov',
                    'avatar': 'marcelopetrov',
                    'is_online': false
                },
                {
                    'id': 10,
                    'first_name': 'Ismail',
                    'last_name': 'Botobo',
                    'avatar': 'ismailbotobo',
                    'is_online': false
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

const getMessagesList = (receiverId, pageNumber) => {
    const getChatUrl = `${appPath}${receiverId}/${pageNumber}/`;
    return axios.get(getChatUrl);
};

const postChatMessage = (receiverId, text) => {
    const postChatUrl = `${appPath}${receiverId}/`;
    return axios.post(postChatUrl, {
        'text': text
    });
};

const getOnlineUsers = users => {
    const getOnlineUsersUrl = `${appPath}online/`;
    return axios.post(getOnlineUsersUrl, {
        users: users
    });
};

export {getReceiversList, getMessagesList, postChatMessage, getOnlineUsers};
