import axios from 'axios';
import { apiUrl } from 'src/helper';


const eventPath = apiUrl + 'events/';
const teamPath = apiUrl + 'team/';
const userPath = apiUrl + 'user/';

export const getVotes = (eventId) => {
    return axios.get(apiUrl + 'events/' + eventId + '/vote/');
};

export const getAnswersWithMembers = (eventId, voteId) => {
    return axios.get(eventPath + eventId + '/vote/' + voteId + '/answers_with_members/');
};

export const getAnswers = (eventId, voteId) => {
    return axios.get(apiUrl + 'events/' + eventId + '/vote/' + voteId + '/answer/');
};

export const putAnswer = (teamId, eventId, voteId, answerId, members) => {
    const url = apiUrl + 'team/'    + teamId +
                         '/event/'  + eventId +
                         '/vote/'   + voteId +
                         '/answer/' + answerId + '/';
    return axios.put(url, {members: members});
};

export const postVote = (data) => {
    const url = apiUrl + 'events/' + data.event + '/vote/';
    return axios.post(url, data);
};

export const postAnswer = (answer, eventId, voteId) => {
    const url = apiUrl + 'events/' + eventId + '/vote/' + voteId + '/answer/';
    const data = {
        'text': answer,
        'vote': voteId,
        'members': []
    };
    return axios.post(url, data);
};

export const deleteCustomVote = (teamId, eventId, voteId) => {
    const url = teamPath + teamId + '/event/' + eventId + '/vote/' + voteId;
    return axios.delete(url);
};
