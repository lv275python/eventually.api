import {apiUrl} from 'src/helper';
import axios from 'axios';

const appPath = apiUrl + 'chat/';

const getMentorsListService = () => {
    const url = apiUrl + 'mentor/mentors_list/';
    return axios.get(url);
};

const getStudentsListService = () => {
    const url = apiUrl +'mentor/students_list/';
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
