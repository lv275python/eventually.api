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
        };
    }

    handleEmail = event => {
        const regex = /^\S+@\S+\.\S+$/;
        if(regex.test(event.target.value) === true )
        {
            this.setState({MessageEmail: '', email: event.target.value});
        }
        else {
            this.setState({ MessageEmail: 'Error Email'});
        }
    };

    handlePassword = event => {
        const regexp = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
        if(regexp.test(event.target.value) === true )
        {
            this.setState({MessagePassword: '', password: event.target.value});
        }
        else {
            this.setState({ MessagePassword: 'Error Password' });
        }
    };

    handleSubmit = event => {
        const email = this.state.email;
        const password = this.state.password;
        registerService(email, password)
            .then((response) => {
                this.props.history.push('/login');
            });
        event.preventDefault();
    };

    render() {
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
                />
            </div>
        );
    }
}

export default withRouter(Register);
