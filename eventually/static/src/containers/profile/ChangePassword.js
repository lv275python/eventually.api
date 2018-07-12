import React from 'react';
import TextField from 'material-ui/TextField';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import {changePasswordService} from './ProfileService';
import {getUserId, validatePassword} from 'src/helper';

const MsgErrorValidatePassword = `Password must contain at least 6 characters: uppercase characters (A-Z);
                                              lowercase characters (a-z); digits (0-9)`;
const MsgErrorConfirmPassword = 'Confirm new password have to be the same as new password';


export default class ChangePassword extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            oldPass: '',
            newPass: '',
            ConfPass: '',
            open: false,
            errMsgOldPass: '',
            errMsgNewPass: '',
            errMsgConfPass: ''
        };
    }

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

    handleChange = () => {
        changePasswordService(
            getUserId(),
            this.state.oldPass,
            this.state.newPass
        ).then(() => {
            this.handleClose();
        }).catch(() => {
            //error handle
            this.handleClose();
        });
    };

    handleChangeOldPassword = (event) => {
        let errMsgOldPass = validatePassword(event.target.value)? '' : MsgErrorValidatePassword;
        this.setState({
            oldPass: event.target.value,
            errMsgOldPass: errMsgOldPass
        });
    };

    handleChangeNewPassword = (event) => {
        let errMsgNewPass = validatePassword(event.target.value)? '' : MsgErrorValidatePassword;
        let errMsgConfPass = (event.target.value == this.state.ConfPass) ? '' : MsgErrorConfirmPassword;
        this.setState({
            newPass: event.target.value,
            errMsgNewPass: errMsgNewPass,
            errMsgConfPass: errMsgConfPass
        });
    };

    handleChangeConfirmNewPassword = (event) => {
        let errMsgConfPass = (this.state.newPass == event.target.value) ? '' : MsgErrorConfirmPassword;
        this.setState({
            ConfPass: event.target.value,
            errMsgConfPass: errMsgConfPass
        });
    };
    isValid = () => {
        let result = validatePassword(this.state.oldPass) &&
                     validatePassword(this.state.newPass) &&
                     (this.state.newPass == this.state.ConfPass);
        return result;
    };

    render(){

        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleChange}
                disabled={!this.isValid()}
            />,
        ];

        return(
            <div>
                <RaisedButton
                    label="Change password"
                    primary={true}
                    keyboardFocused={true}
                    onClick={this.handleOpen}
                />

                <Dialog
                    title="Dialog With Actions"
                    actions={actions}
                    modal={true}
                    open={this.state.open}
                >
                    <TextField
                        hintText="Old Password"
                        floatingLabelText="Old Password"
                        type="password"
                        onChange={this.handleChangeOldPassword}
                        errorText={this.state.errMsgOldPass}
                    /><br/>
                    <TextField
                        hintText="New Password"
                        floatingLabelText="New Password"
                        type="password"
                        onChange={this.handleChangeNewPassword}
                        errorText={this.state.errMsgNewPass}
                    /><br/>
                    <TextField
                        hintText="Confirm New Password"
                        floatingLabelText="Confirm New Password"
                        type="password"
                        onChange={this.handleChangeConfirmNewPassword}
                        errorText={this.state.errMsgConfPass}
                    />
                </Dialog>
            </div>
        );
    }
}
