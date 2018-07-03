import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Home from './containers/Home';
import Profile from './containers/profile/Profile';
import UserProgress from './containers/userProgress/ProgressProfile';
import Item from './containers/item/Item';
import CurriculumList from './containers/curriculum/CurriculumList';
import TopicView from './containers/topicList/TopicView';
import MentorItem from './containers/mentorItem/MentorItem';
import MentorDashboard from './containers/mentorDashboard/MentorDashboard';
import EventList from './containers/event/EventList';
import EventDetails from './containers/event/EventDetails';
import Task from './containers/taskItem/Task';
import VoteBox from './containers/voting/VoteBox';
import SuggestedTopics from './containers/suggestedtopics/SuggestedTopics';
import MentorBoard from './containers/MentorBoard/MentorBoard';


export default class MainRouter extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route path='/home' component={Home} />
                    <Route path='/profile/:profileId' component={Profile}/>
                    <Route path='/progress' component={UserProgress}/>
                    <Route path='/curriculums/:curriculumId/topics/:topicId' component={TopicView}/>
                    <Route path='/curriculums' component={CurriculumList}/>
                    <Route path='/item/:itemId' component={Item} />
                    <Route path='/mentoritem' component={MentorItem}/>
                    <Route path='/dashboard' component={MentorDashboard}/>
                    <Route path='/events/:eventId/task/:taskId' component={Task}/>
                    <Route path='/events/:eventId/vote' component={VoteBox}/>
                    <Route path='/events/:eventId' component={EventDetails}/>
                    <Route path='/events' component={EventList}/>
                    <Route path='/suggestedtopics' component={SuggestedTopics}/>
                    <Redirect path='*' to='/home' />
                </Switch>
            </main>
        );
    }
}
