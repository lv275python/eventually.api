import axios from 'axios';
import {apiUrl} from 'src/helper';

const curriculumPath = apiUrl + 'curriculums/';
const mentorPath = apiUrl + 'mentor/';

const getCurriculumsService = () => {
    return axios.get(curriculumPath);
};

const getTopicsService = () => {
    return axios.get(mentorPath);
};

const IsMentorService = (curriculumId, topicId) => {
    let url = curriculumPath + curriculumId + '/topics/' + topicId + '/is_mentor/';
    return axios.get(url);
};

export {getCurriculumsService, getTopicsService} ;