import axios from 'axios';

const getOwner = (id) => {
    return axios.get('/api/v1/user/'+id+'/');
};
const getTeam = (id) => {
    return axios.get('/api/v1/team/'+id +'/');
};

export { getOwner, getTeam };
