import {apiUrl} from 'src/helper';
import axios from 'axios';

const appPath = apiUrl + 'suggestedtopics/'

const getSuggestedTopicsService = () => {
    return axios.get(appPath);
};

const putSuggestedTopicsItem = (id, name, description, interestedUser, removeInterest) => {
    return axios.put(appPath + id + '/', {name, description, 'interested_user': interestedUser, 'remove_interest': removeInterest})
    };

const postSuggestedTopicsItem = (data) => {
    const url = appPath
    return axios.post(url, data);
};

export {getSuggestedTopicsService, putSuggestedTopicsItem, postSuggestedTopicsItem};