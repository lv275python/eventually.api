import axios from "axios"


export const profileURL = '/api/v1/user/user_id/profile/';

export const putProfileService = (first_name, middle_name, last_name, hobby, photo, birthday) => {
        return axios.put(profileURL, {
            first_name, 
            middle_name, 
            last_name,
            hobby,
            photo,
            birthday,
        });
    };
