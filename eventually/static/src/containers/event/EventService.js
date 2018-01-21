import axios from 'axios';


const eventURL = '/api/v1/events/';
const teamURL = '/api/v1/team/';

export const getEvents = () => {
    return axios.get('/api/v1/events/');

};

export const getEventService = id => {
    let url = eventURL+ id + '/';
    return axios.get(url);
};


export const putEventService = (eventId, teamId, name, description, start_at, budget, status) => {

    let url = eventURL + eventId + '/';
    return axios.put(url, {
        teamId,
        name,
        description,
        start_at,
        budget,
        status
    });
};

const getTeamService = () => {
    return axios.get(teamURL);
};

