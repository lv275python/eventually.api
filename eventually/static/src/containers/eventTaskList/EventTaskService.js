import axios from 'axios';
import {apiUrl} from'../../helper/utils';


const rootUrl = '/api/v1/';
const eventPath = rootUrl + 'events/';
const teamPath = rootUrl + 'team/';
const userPath = rootUrl + 'user/';

const eventServiceGet = event_id => {
    let url = eventPath+event_id+'/';
    return axios.get(url);
};

const eventTasksServiceGet = event_id => {
    let url = eventPath+event_id+'/task/';
    return axios.get(url);
};

const taskGetTeamService = (team_id, full_name) => {
    let url = teamPath + team_id + '/';
    if (full_name) url+='?full_name=true';
    return axios.get(url);
};

const eventTaskServicePut = (event_id, task_id, data) => {
    let url = eventPath + event_id + '/task/' + task_id + '/';
    return axios.put(url, data);
};

const eventTaskServicePost = (eventId, data) => {
    let url = eventPath + eventId + '/task/';
    return axios.post(url, data);
};


export { eventTasksServiceGet, taskGetTeamService, eventTaskServicePut, eventTaskServicePost, eventServiceGet };

