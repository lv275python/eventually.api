import axios from 'axios';
import {apiUrl} from'../../helper/utils';

const eventTaskServicePost = (eventId, data) => {
    let url = apiUrl + 'events/' + eventId + '/task/';
    return axios.post(url, data);
};

const getTeamService = (teamId, full_name) => {
    let url = apiUrl + 'team/' + teamId + '/';
    if (full_name){
        url += '?full_name=true';
    }
    console.log(url);
    console.log(full_name);
    return axios.get(url);
};

const getUserService = id => {
    let url = apiUrl + 'user/' + id +'/';
    return axios.get(url);
};

export { eventTaskServicePost, getTeamService, getUserService };
