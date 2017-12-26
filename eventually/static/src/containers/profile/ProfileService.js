import axios from "axios"


export const profileURL = '/api/v1/user/user_id/profile/';
export const userURL = '/api/v1/user/user_id/';

export const putProfileService = (hobby,birthday) => {
        return axios.put(profileURL, {
            hobby,
            birthday,
        });
    };

export const userProfileService = (first_name, middle_name, last_name) => {
        return axios.put(userURL, {
            first_name, 
            middle_name, 
            last_name,
        });
    };

export const getProfileService = (user_id) => {
	return axios.get(profileURL);
}