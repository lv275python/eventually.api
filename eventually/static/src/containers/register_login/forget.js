import React from 'react';
import {withRouter} from 'react-router-dom'
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {forgetPasswordService} from './registrationService.js'

const style = {
  margin: 12,
};
class Forget extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email:'',
    };
  }

  handleEmail = event => {
    this.setState({email: event.target.value});
  }

  handleSubmit = event => {
     const email = this.state.email;
     forgetPasswordService(email)
   }

  render() {
    return(
      <div style={style} >
        <h2>Email</h2>
        <TextField onChange={this.handleEmail}
                   hintText='example@example.com'
        /><br />
        <br />
        <RaisedButton label='Send mail to email'
                      primary={true}
                      onClick={this.handleSubmit}
        />
      </div>
    );
  };
};

export default withRouter(Forget)
