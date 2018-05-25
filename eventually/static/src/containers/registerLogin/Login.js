import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {orange500} from 'material-ui/styles/colors';

import {loginService} from './registrationService';

const style = {
    margin: 12,
};

const errorStyle = {
    color: orange500,
};

class Login extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: '',
            MessageEmail: '',
            MessagePassword: '',
            messageError: false,
        };
    }

    componentDidCatch(error, info) {
        console.log(info);
        console.log(error);
    }

    handleEmail = event => {
        const regex = /^\S+@\S+\.\S+$/;
        if(regex.test(event.target.value) === true) {
            this.setState({MessageEmail: '', email: event.target.value});
        }
        else {
            this.setState({ MessageEmail: 'Error Email'});
        }
    };

     handlePassword = event => {
         const regexp = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
         if(regexp.test(event.target.value) === true) {
             this.setState({MessagePassword: '', password: event.target.value});
         }
         else {
             this.setState({ MessagePassword: `Password must contain at least 6 characters: uppercase characters (A-Z);
                                               lowercase characters (a-z); digits (0-9)`});
         }
     };

    handleSubmit = event => {
        const email = this.state.email;
        const password = this.state.password;
        loginService(email, password)
            .then((response) => {
                if (response.status === 400) {
                    this.setState({messageError:true});
                } else {
                    this.props.history.push('/home');
                }
            });
        event.preventDefault();

    };

    render() {
        let loginError;
        if (this.state.messageError === true) {
            loginError = (
                <div>
                    <p style={errorStyle}>Invalid email or password</p>
                </div>
            );
        }

        return (
            <div style={style}>
                <h2>Email</h2>
                <TextField
                    onChange={this.handleEmail}
                    hintText='email'
                    errorText={this.state.MessageEmail}
                    errorStyle={errorStyle}
                /><br/>
                <br/>
                <h2>Password</h2>
                <TextField
                    onChange={this.handlePassword}
                    hintText='password'
                    errorText={this.state.MessagePassword}
                    errorStyle={errorStyle}
                    type="password"
                /><br/>
                <RaisedButton
                    label='Login'
                    primary={true}
                    onClick={this.handleSubmit}
                    disabled={(this.state.email === '' || this.state.MessageEmail !== '' || this.state.password === ''
                        || this.state.MessagePassword !== '')}
                />
                {loginError}
            </div>
        );
    }
}


export default withRouter(Login);
