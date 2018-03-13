import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {forgetPasswordService} from './registrationService.js';
import {orange500} from 'material-ui/styles/colors';

const style = {
    margin: 12,
};

const errorStyle = {   
    color: orange500,
};

class Forget extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            email: '',
            MessageEmail: '',
        };
    }

     handleEmail = event => {

         const regex = /^\S+@\S+\.\S+$/;
         if(regex.test(event.target.value) === true )
         {
             this.setState({MessageEmail: '', email: event.target.value});
         }
         else {
             this.setState({ MessageEmail: `Invalid Email`});
         }
     };

    handleSubmit = event => {
        const email = this.state.email;
        forgetPasswordService(email);
    };

    render() {
        return(
            <div style={style} >
                <h2>Email</h2>
                <TextField onChange={this.handleEmail}
                    hintText='example@example.com'
                    errorText={this.state.MessageEmail}
                    errorStyle={errorStyle}
                /><br />
                <br />
                <RaisedButton label='Send mail to email'
                    primary={true}
                    onClick={this.handleSubmit}
                />
            </div>
        );
    }
}

export default withRouter(Forget);
