import React from 'react';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import {Tabs, Tab} from 'material-ui/Tabs';
import Login from './login.js';
import Logout from './logout.js';
import Register from './register.js';
import Forget from './forget.js';

export default class Sign extends React.Component {
  render() {
    return (
      <MuiThemeProvider>
        <Tabs>
          <Tab label="Register" >
            <Register />
          </Tab>
          <Tab label="Login" >
            <Login />
          </Tab>
          <Tab label="Forget password">
            <Forget />
          </Tab>
          <Tab label="Logout">
            <Logout />
          </Tab>
        </Tabs>
      </MuiThemeProvider>
    );
  }
}
