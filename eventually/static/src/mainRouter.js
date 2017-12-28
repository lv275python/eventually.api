import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Home from './containers/Home';
import UserProgress from './containers/userProgress/UserProgress';
import Item from './containers/item/Item';
import CurriculumList from './containers/curriculum/CurriculumList';
import MentorItem from './containers/mentor_item/MentorItem';
import MentorDashboard from './containers/mentorDashboard/MentorDashboard';
import TeamList from './containers/teamList/TeamList';

export default class MainRouter extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route path='/home' component={Home} />
                    <Route path='/progress' component={UserProgress}/>
                    <Route path='/curriculums' component={CurriculumList}/>
                    <Route path='/item/:itemId' component={Item} />
                    <Route path='/mentoritem' component={MentorItem}/>
                    <Route path='/dashboard' component={MentorDashboard}/>
                    <Route path='/teamlist' component={TeamList}/>
                    <Redirect path="*" to="/home" />
                </Switch>
            </main>
        );
    }
}
