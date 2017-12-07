import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Home from './containers/Home';
import Profile from './containers/profile/Profile';
import Item from './containers/item/Item'
import TopicList from './containers/topicList/TopicList'

export default class MainRouter extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                  <Route path='/home' component={Home} />
                  <Route path='/profile' component={Profile} />
                  <Route path='/item/:itemId' component={Item} />
                  <Route path='/topiclist' component={TopicList} />                 
                  <Redirect path="*" to="/home" />
                </Switch>
            </main>
        )
    }
}
