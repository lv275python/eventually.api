import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {logoutService} from './registrationService.js'

const style = {
  margin: 12,
};

export default class Logout extends React.Component {
  constructor(props) {
    super(props);
  }
  handleSubmit = event => {
     logoutService()
   }
  render() {
    return(
      <div style={style} >
        <RaisedButton label='Logout'
                      primary={true}
                      onClick={this.handleSubmit}
        />
      </div>
    );
  };
};
