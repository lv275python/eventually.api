import axios from 'axios';

const url = '/api/v1/team/';

const GetTeamsListService = () => axios.get(url);

const PostEventService = (data) => {
    const url = '/api/v1/team/' + data.team + '/event/';
    axios.post(url, data);
};

export { GetTeamsListService, PostEventService };
