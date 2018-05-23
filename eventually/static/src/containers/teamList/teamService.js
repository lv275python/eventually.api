import {apiUrl} from 'src/helper';
import axios from 'axios';

const appPath = apiUrl + 'team/';
const getMembers = apiUrl +  'user/';
const getUsers = apiUrl +'user/all/';

const teamServicePost = (data) => {
    let url = appPath + 'new/';
    return axios.post(url, data);
};

const usersServiceGet = () => {
    return axios.get(getUsers);
};

const teamServiceGet = (full_name) => {
    const path = appPath + '?full_name='+full_name;
    return axios.get(path);
};

const teamServiceGetMembers = id => {
    return axios.get(getMembers+id+'/');
};

const teamServicePut = (id, name, description, image) => {
    return axios.put(appPath + id + '/', {name, description, image});
};

const teamServiceDelete = id => {
    return axios.delete(appPath + id + '/')
        .catch(error => {return(error.response);});
};

const getMemberName = (user) => {
    if (user['first_name'] || user['last_name']){
        return (user['first_name'] + '  ' + user['last_name']);
    } else {
        return user['email'].match(/^(.+)@/)[1];
    }
};


export {teamServiceGet, teamServicePut, teamServiceGetMembers, teamServicePost, usersServiceGet, teamServiceDelete, getMemberName};
