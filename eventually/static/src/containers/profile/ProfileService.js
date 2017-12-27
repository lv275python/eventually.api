import axios from 'axios';


export const profileURL = '/api/v1/user/';

export const putProfileService = (id, first_name, middle_name, last_name, hobby, photo, birthday) => {
    let url = profileURL + id + '/profile/';
    return axios.put(url, {
        first_name, 
        middle_name, 
        last_name,
        hobby,
        photo,
        birthday,
    });
};

export const getProfileService = id => {
    let url = profileURL;
    if (id){
        url += id + '/';
    } 
    url += 'profile/';
    return axios.get(url);
};
