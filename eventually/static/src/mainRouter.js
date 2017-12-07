import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Sign from './containers/register_login/sign';
import Home from './containers/home';
import Profile from './containers/profile/Profile';

export default class MainRouter extends React.Component {
    render() {
        return (
            <main>
                <Switch>
                  <Route path='/home' component={Home} />
                  <Route path='/profile' component={Profile} />
                  <Redirect path='*' to='/home' />
                </Switch>
            </main>
        )
    }
}
