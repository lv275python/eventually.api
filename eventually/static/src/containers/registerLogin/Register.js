import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {registerService} from './registrationService.js';
import {orange500, blue500, green700,pink600} from 'material-ui/styles/colors';

const style = {
    margin: 12,
};

const errorStyle = {
    color: orange500,
};

class Register extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            email: '',
            password: '',
            MessageEmail: '',
            MessagePassword: '',
            errorRegister: false,
        };
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
        registerService(email, password).then((response) => {
            this.setState({errorRegister: false});
            this.props.history.push('/login');
        }).catch((error) => {
            this.setState({errorRegister: true});
        });
        event.preventDefault();
    };

    render() {
        let errorRegister;
        if (this.state.errorRegister === true) {
            errorRegister = (
                <div>
                    <p style={errorStyle}>This mail is already registered</p>
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
                    type="email"
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
                    label='Register'
                    primary={true}
                    onClick={this.handleSubmit}
                    disabled={(this.state.email === '' || this.state.MessageEmail !== '' || this.state.password === ''
                        || this.state.MessagePassword !== '')}
                />
                {errorRegister}
            </div>
        );
    }
}

export default withRouter(Register);
