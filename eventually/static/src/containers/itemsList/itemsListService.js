import axios from 'axios';
import { apiUrl } from 'src/helper';

const assignmentPath = apiUrl + 'assignment/list/'

const getItemsList = (topicId, userId) => {
    let url;
    if (userId){
        url = assignmentPath + topicId + '/' + userId;
    } else {
        url = assignmentPath + topicId;
    }
    return axios.get(url);
};

export default getItemsList;
