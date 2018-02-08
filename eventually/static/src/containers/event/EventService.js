import axios from 'axios';
import {apiUrl} from 'src/helper';

const eventPath = apiUrl + 'events/';
const teamPath = apiUrl + 'team/';
const userPath = apiUrl + 'user/';

export const getEvents = () => {
    return axios.get(eventPath);
};

export const putEventService = (eventId, teamId, name, description, start_at, budget, status, duration) => {
    let url = eventPath + eventId + '/';
    return axios.put(url, {
        teamId,
        name,
        description,
        start_at,
        budget,
        status,
        duration
    });
};

export const getTeamService = () => {
    return axios.get(teamPath);
};

export const eventServiceGet = event_id => {
    let url = eventPath + event_id + '/';
    return axios.get(url);
};

export const eventTasksServiceGet = event_id => {
    let url = eventPath + event_id + '/task/';
    return axios.get(url);
};

export const taskGetTeamService = (team_id, full_name) => {
    let url = teamPath + team_id + '/';
    if (full_name) url += '?full_name=true';
    return axios.get(url);
};

export const eventTaskServicePut = (event_id, task_id, data) => {
    let url = eventPath + event_id + '/task/' + task_id + '/';
    return axios.put(url, data);
};

export const eventTaskServicePost = (eventId, data) => {
    let url = eventPath + eventId + '/task/';
    return axios.post(url, data);
};

export const getOwner = (id) => {
    return axios.get(userPath+id+'/');
};

export const GetTeamsListService = () => axios.get(teamPath);

export const PostEventService = (data) => {
    const url = teamPath + data.team + '/event/';
    axios.post(url, data);
};
