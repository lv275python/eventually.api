import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {putNewPasswordService} from './registrationService';
import {orange500} from 'material-ui/styles/colors';

const style = {
    margin: 12,
};

const errorStyle={
    position: 'relative',
    color: orange500,
};

class SetNewPassword extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            password: '',
            confirmPassword: '',
            token: this.props.match.params.token,
            messagePassword:'',
            changeButtonStatus: true,
        };
    }

    handlePassword = event => {
        const regexp = /^(?=.*[0-9])(?=.*[A-Z])[a-zA-Z0-9!@#$%^&*]{6,16}$/;
        regexp.test(event.target.value) === true ? this.setState({
            messagePassword: '', password: event.target.value}):
            this.setState({messagePassword: `Password must contain at least 6 characters: uppercase characters (A-Z);
                                             lowercase characters (a-z); digits (0-9)`
            });
    };


    handleConfirmPassword = event => {
        this.setState({confirmPassword: event.target.value});
    };

    handleSubmit = event => {
        const newPassword = this.state.password ;
        const token = this.state.token;
        putNewPasswordService(token, newPassword).then((response) => {
            this.props.history.push('/login');
        });
    };

    render() {
        return(
            <div style={style} >
                <h2>New Password</h2>
                <TextField
                    onChange={this.handlePassword}
                    hintText='Enter password'
                    type="password"
                    errorStyle = {errorStyle}
                    errorText={this.state.messagePassword}
                />
                <br />
                <h2>Confirm Password</h2>
                <TextField
                    onChange={this.handleConfirmPassword}
                    hintText='Re-enter password'
                    type="password"
                    errorStyle = {errorStyle}
                />
                <br />
                <br />
                <RaisedButton label='Change password'
                    primary={true}
                    onClick={this.handleSubmit}
                    disabled={this.state.password == this.state.confirmPassword ? false : true}

                />
            </div>
        );
    }
}


export default withRouter(SetNewPassword);
