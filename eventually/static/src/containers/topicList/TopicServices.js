import axios from 'axios';
import { apiUrl } from 'src/helper';


const curriculumPath = apiUrl + 'curriculums/';
const mentorPath = apiUrl + 'mentor/';

const postTopicService = (curriculumId, data) => {
    let url = curriculumPath + curriculumId + '/topics/';
    return axios.post(url, data);
};

const postTopicAssignService = data => {
    return axios.post(mentorPath, data);
};

const getTopicStudentsService = topicId => {
    let url = mentorPath + 'is_student/' + topicId + '/';
    return axios.get(url);
};

const getIsMentorService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/is_mentor/';
    return axios.get(url);
};

const getTopicDetailService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/';
    return axios.get(url);
};

const deleteTopicService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/';
    return axios.delete(url);
};

const getItemListService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/items/';
    return axios.get(url);
};

const deleteMenteeService = topicId => {
    let url = mentorPath + 'delete/' + topicId + '/';
    return axios.delete(url);
};

export {
    deleteTopicService,
    postTopicService,
    postTopicAssignService,
    getTopicStudentsService,
    deleteMenteeService,
    getIsMentorService,
    getTopicDetailService,
    getItemListService
};
