import axios from 'axios';

const appPath = '/api/v1/team/';
const getMembers = '/api/v1/user/';

const teamServiceGet = () => {
    return axios.get(appPath);
};

const teamServiceGetMembers = id => {
    return axios.get(getMembers+id+'/');
};

const teamServicePut = (id, name, description, image) => {
    return axios.put(appPath + id + '/', {name, description, image});
};

export {teamServiceGet, teamServicePut, teamServiceGetMembers};
