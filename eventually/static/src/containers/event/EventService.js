import axios from 'axios';

const getEvents = () => {
    return axios.get('/api/v1/events/');

};

export { getEvents };
