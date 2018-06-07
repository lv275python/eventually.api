import {apiUrl} from 'src/helper';
import axios from 'axios';


const appPath = apiUrl + 'suggestedtopics/';
const topicAllTitlePath = apiUrl + 'topic/all_title/';

const getSuggestedTopicsService = () => {
    return axios.get(appPath);
};

const getTopicAllTitleService = () => {
    return axios.get(topicAllTitlePath);
};

const putSuggestedTopicsItem = (id, name, description, interestedUser, removeInterest) => {
    const data = {
        name,
        description,
        'interested_user': interestedUser,
        'remove_interest': removeInterest
    };
    return axios.put(appPath + id + '/', data);
};

const postSuggestedTopicsItem = data => {
    const url = appPath;
    return axios.post(url, data);
};

const deleteSuggestedTopicsItem = (id, name, description) => {
    const data = {
        name,
        description
    };
    return axios.delete(appPath + id + '/', data);
};

export {getSuggestedTopicsService, getTopicAllTitleService, putSuggestedTopicsItem, postSuggestedTopicsItem, deleteSuggestedTopicsItem};
