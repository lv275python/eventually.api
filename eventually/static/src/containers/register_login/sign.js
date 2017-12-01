import React from 'react';
import {Link} from "react-router-dom";
import {Tabs, Tab} from 'material-ui/Tabs';
import Login from './login.js';
import Register from './register.js';
import Forget from './forget.js';
import {withRouter} from 'react-router-dom'


class Sign extends React.Component {
  constructor(props) {
    super(props);
  }

  toRegister = () => {
    this.props.history.push('/register')
  }
  toLogin = () => {
    this.props.history.push('/login')
  }
  toForgetPassword= () => {
    this.props.history.push('/forget')
  }
  render() {
    return (
      <Tabs>
        <Tab label="Register"  onActive={this.toRegister}>
        </Tab>
        <Tab label="Login" onActive={this.toLogin}>
        </Tab>
        <Tab label="Forget password" onActive={this.toForgetPassword}>
        </Tab>
      </Tabs>

    )
  }
}
export default withRouter(Sign)
