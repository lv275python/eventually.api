import axios from 'axios';


const eventURL = '/api/v1/events/';
const teamURL = '/api/v1/team/';

export const getEvents = () => {
    return axios.get('/api/v1/events/');
};

export const putEventService = (eventId, teamId, name, description, start_at, budget, status, duration) => {

    let url = eventURL + eventId + '/';
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

const getTeamService = () => {
    return axios.get(teamURL);
};

