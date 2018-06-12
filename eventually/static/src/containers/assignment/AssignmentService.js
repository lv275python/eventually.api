import axios from 'axios';
import { apiUrl } from 'src/helper/index';


const assignmentPath = apiUrl + 'assignment/';


const getAssignmentCurriculumService = () => {
    let url = assignmentPath + 'curriculums/';
    return axios.get(url);
};

const getAssignmentTopicListService = curriculumId => {
    let url = assignmentPath + curriculumId + '/topics/';
    return axios.get(url);
};


export {getAssignmentCurriculumService, getAssignmentTopicListService, };
