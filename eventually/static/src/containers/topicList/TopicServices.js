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

const getTopicStudentsService = (topicId) =>{
    let url = mentorPath + 'is_student/' + topicId + '/';
    return axios.get(url);
};

const getIsMentorService = (curriculumId, topicId) =>{
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/is_mentor/';
    return axios.get(url);
};

const deleteMenteeService = (topicId) => {
    let url = mentorPath + 'delete/' + topicId + '/';
    return axios.delete(url);
};

export { postTopicService, postTopicAssignService, getTopicStudentsService, deleteMenteeService, getIsMentorService };
