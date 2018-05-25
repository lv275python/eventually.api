import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';
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
            sentLetter : false,
            messageError: false,
        };
    }

     handleEmail = event => {

         const regex = /^\S+@\S+\.\S+$/;
         if(regex.test(event.target.value) === true )
         {
             this.setState({MessageEmail: '', email: event.target.value});
         }
         else {
             this.setState({ MessageEmail: 'Invalid email.'});
         }
     };

    handleSubmit = event => {
        const email = this.state.email;
        forgetPasswordService(email).then((response) => {
            this.setState({messageError: false, sentLetter: true});
        }).catch((error) => {
            this.setState({messageError: true, sentLetter: false});
        });
    };

    handleReturn = event => {
        this.setState({sentLetter: false});
    };

    render() {
        let messageError;
        if (this.state.messageError === true) {
            messageError = (
                <div>
                    <p style={errorStyle}>Invalid email</p>
                </div>
            );
        }

        if (this.state.sentLetter === false) {
            return (
                <div style={style}>
                    <h2>Email</h2>
                    <TextField onChange={this.handleEmail}
                        hintText='example@example.com'
                        errorText={this.state.MessageEmail}
                        errorStyle={errorStyle}
                    /><br/>
                    <br/>
                    <RaisedButton label='Send mail to email'
                        primary={true}
                        onClick={this.handleSubmit}
                        disabled={this.state.email === '' || this.state.MessageEmail !== ''}
                    />
                    {messageError}
                </div>
            );
        } else {
            return (
                <div style={style}>
                    <h2>Сheck your mail</h2>
                    <FlatButton label='OK'
                        primary={true}
                        onClick={this.handleReturn}
                    />
                </div>
            );
        }
    }
}


export default withRouter(Forget);
