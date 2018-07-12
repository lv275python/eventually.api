import React from 'react';
import {withRouter} from 'react-router-dom';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {putNewPasswordService} from './registrationService';
import {orange500} from 'material-ui/styles/colors';
import FlatButton from 'material-ui/FlatButton';
import {validatePassword} from 'src/helper';

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
            expiredTokenError: false,
            messageError: false,
            messageSuccess: false,
        };
    }

    handlePassword = event => {
        validatePassword(event.target.value) === true ? this.setState({
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
            this.setState({messageError: false});
        }).catch((error) => {
            if (error.response.status === 400) {
                this.setState({messageError: true});
            } else if (error.response.status === 498) {
                this.setState({expiredTokenError: true});
            }

        });
    };

    handleReturn = event => {
        this.props.history.push('/forget');
    };

    render() {
        let loginError;
        if (this.state.messageError === true) {
            loginError = (
                <div>
                    <p style={errorStyle}>New password cannot be the same as old</p>
                </div>
            );
        }

        let expiredToken;
        if (this.state.expiredTokenError === true) {
            expiredToken = (
                <div>
                    <p style={errorStyle}>Token has expired</p>
                    <FlatButton
                        label='Send another mail'
                        primary={true}
                        onClick={this.handleReturn}
                    />
                </div>
            );
        }

        if (this.state.expiredTokenError === true) {
            return expiredToken;
        } else if (this.state.messageError === true) {
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
                    {loginError}
                </div>
            );
        } else {
            return ( <div style={style} >
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
                <RaisedButton label='Change password' primary={true}
                    onClick={this.handleSubmit}
                    disabled={this.state.password == this.state.confirmPassword ? false : true}
                />
            </div>
            );
        }
    }
}


export default withRouter(SetNewPassword);
