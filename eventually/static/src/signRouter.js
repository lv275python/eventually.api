import React from "react";
import {Route, Switch, Redirect} from "react-router-dom";
import Register from './containers/register_login/register'
import Login from './containers/register_login/login'
import Forget from './containers/register_login/forget'


export default class SignRouter extends React.Component{
    render() {
        return (
            <main>
              <Switch>
                <Route path='/register' component={Register} />
                <Route path='/login' component={Login} />
                <Route path='/forget' component={Forget} />
                <Redirect path="*" to="/login" />
              </Switch>
            </main>
        )
      }
    }
