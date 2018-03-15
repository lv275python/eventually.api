import axios from 'axios';
import { apiUrl } from 'src/helper';


const curriculumPath = apiUrl + 'curriculums/';
const mentorPath = apiUrl + 'mentor/';

const postItemService = (curriculumId, topicId, data) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/items/';
    return axios.post(url, data);
};

const deleteItemService = (curriculumId, topicId, id) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/items/' + id + '/delete/';
    return axios.delete(url);
};

const getItemListService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/items/';
    return axios.get(url);
};

const putEditItemService = (curriculumId, topicId, id, data) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/items/' + id + '/';
    return axios.put(url, data);
};


export {
    deleteItemService,
    getItemListService,
    postItemService,
    putEditItemService
};
