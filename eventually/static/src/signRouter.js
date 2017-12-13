import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Register from './containers/register_login/Register';
import Login from './containers/register_login/Login';
import Forget from './containers/register_login/Forget';


export default class SignRouter extends React.Component{
    render() {
        return (
            <main>
                <Switch>
                    <Route path='/register' component={Register} />
                    <Route path='/login' component={Login} />
                    <Route path='/forget' component={Forget} />
                    <Redirect path='*' to='/login' />
                </Switch>
            </main>
        );
    }
}
