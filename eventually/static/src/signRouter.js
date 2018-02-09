import React from 'react';
import {Route, Switch, Redirect} from 'react-router-dom';
import Register from './containers/registerLogin/Register';
import Login from './containers/registerLogin/Login';
import Forget from './containers/registerLogin/Forget';
import SetNewPassword from './containers/registerLogin/SetNewPassword';


export default class SignRouter extends React.Component{
    render() {
        return (
            <main>
                <Switch>
                    <Route path='/register' component={Register} />
                    <Route path='/login' component={Login} />
                    <Route path='/forget' component={Forget} />
                    <Route path='/forget_password/:token' component={SetNewPassword} />
                    <Redirect path='*' to='/login' />
                </Switch>
            </main>
        );
    }
}
