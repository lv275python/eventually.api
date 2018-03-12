import { apiUrl } from 'src/helper';
import axios from 'axios';



const eventPath = apiUrl + 'events/';
const teamPath = apiUrl + 'team/';
const userPath = apiUrl + 'user/';

export const getEvent = (eventId) => {
    return axios.get(eventPath + eventId + '/');
};

export const getEvents = (limit, number, dateInSeconds) => {
    return axios.get(eventPath, {
        params: {
            limit: limit,
            number: number,
            from_date: dateInSeconds
        }
    });
};

export const putEventService = (eventId, teamId, name, description, startAt, budget, status, duration) => {
    let url = eventPath + eventId + '/';
    return axios.put(url, {
        teamId,
        name,
        description,
        startAt,
        budget,
        status,
        duration
    });
};

export const getTeamService = () => {
    return axios.get(teamPath);
};

export const eventServiceGet = eventId => {
    let url = eventPath + eventId + '/';
    return axios.get(url);
};

export const eventTasksServiceGet = eventId => {
    let url = eventPath + eventId + '/task/';
    return axios.get(url);
};

export const taskGetTeamService = (teamId, fullName) => {
    let url = teamPath + teamId + '/';
    if (fullName) url += '?full_name=true';
    return axios.get(url);
};

export const eventTaskServicePut = (eventId, taskId, data) => {
    let url = eventPath + eventId + '/task/' + taskId + '/';
    return axios.put(url, data);
};

export const eventTaskServicePost = (eventId, data) => {
    let url = eventPath + eventId + '/task/';
    return axios.post(url, data);
};

export const getOwner = (id) => {
    return axios.get(userPath+id+'/');
};

export const getTeamsListService = () => axios.get(teamPath);

export const postEventService = (data) => {
    const url = teamPath + data.team + '/event/';
    return axios.post(url, data);
};

export const deleteTaskService = (eventId, taskId) => {
    const url = eventPath + eventId + '/task/' + taskId + '/';
    return axios.delete(url);
};
