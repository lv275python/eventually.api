import axios from 'axios';
import {apiUrl} from 'src/helper';


export const appPath = apiUrl + 'user/';

export const putProfileService = (id, first_name, middle_name, last_name, hobby, photo, birthday) => {
    let url = appPath + id + '/profile/';
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
    const profileUrl = `${appPath}${id}/profile/`;
    return axios.get(profileUrl);
};

