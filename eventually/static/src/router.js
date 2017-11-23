import React from "react";
import {Route, Switch} from "react-router-dom";
import Sign from './containers/register_login/sign'

export default class MainRouter extends React.Component{
    render() {
        return (
            <main>
                <Switch>
                  <Route exact path='/' component={Sign} />
                </Switch>

            </main>
        )
    }
}
