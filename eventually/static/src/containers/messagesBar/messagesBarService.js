import axios from 'axios';

const appPath = '/api/v1/chat/';

const getMentorsListService = () => {
    const url = '/api/v1/mentor/mentors_list/';
    return axios.get(url);
};

const getStudentsListService = () => {
    const url = '/api/v1/mentor/students_list/';
    return axios.get(url);
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

export {getMessagesList, postChatMessage, getOnlineUsers, getMentorsListService, getStudentsListService};
