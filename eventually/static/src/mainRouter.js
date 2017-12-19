import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Home from './containers/Home';
import Profile from './containers/profile/Profile';
import Item from './containers/item/Item';
import Curriculum from './containers/curriculum/Curriculum';
import MentorItem from './containers/mentor_item/MentorItem';
export default class MainRouter extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                    <Route path='/home' component={Home} />
                    <Route path='/profile' component={Profile}/>
                    <Route path='/curriculum' component={Curriculum}/>
                    <Route path='/item/:itemId' component={Item} />
                    <Route path='/mentoritem' component={MentorItem}/>
                    <Redirect path="*" to="/home" />
                </Switch>
            </main>
        );
    }
}
