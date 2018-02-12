import axios from 'axios';
import { apiUrl } from 'src/helper';


const curriculumPath = apiUrl + 'curriculums/';


const getCurriculumsService = () => {
    return axios.get(curriculumPath);
};

const getTopicListService = curriculumId => {
    let url = curriculumPath + curriculumId + '/topics/';
    return axios.get(url);
};

const postCurriculumService = data => {
    return axios.post(curriculumPath, data);
};


export { getCurriculumsService, getTopicListService, postCurriculumService };
