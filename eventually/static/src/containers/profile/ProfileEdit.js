import React from 'react';
import {putProfileService} from './ProfileService.js';

import TextField from 'material-ui/TextField';
import FlatButton from 'material-ui/FlatButton'
import DatePicker from 'material-ui/DatePicker';



export default class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            first_name: this.props.first_name,
            middle_name: this.props.middle_name,
            last_name: this.props.last_name,
            first_hobby: this.props.hobby,
            birthday: this.props.birthday,

        };
    };

    handleFirstName = event => {
        this.setState({first_name: event.target.value});

    }

    handleMiddleName = event => {
        this.setState({middle_name: event.target.value});

    }

    handleLastName = event => {
        this.setState({last_name: event.target.value});

    }

    handleHobby = event => {
        this.setState({hobby: event.target.value});

    }

    handleBirthday = (event, date) => {
        this.setState({birthday: date});
    }
    profileEdit = () => {
        const first_name = this.state.first_name;
        const middle_name = this.state.middle_name;
        const last_name = this.state.last_name;
        const hobby = this.state.hobby;
        const birthday = this.state.birthday;
        putProfileService(first_name, middle_name, last_name, hobby,birthday)
        .then(this.props.getProfile());
    }
    
    handleSave = event => {
        const first_name = this.state.first_name;
        const middle_name = this.state.middle_name;
        const last_name = this.state.last_name;
        const hobby = this.state.hobby;
        const birthday = this.state.birthday;
        putProfileService(first_name, middle_name, last_name, hobby,birthday)
        .then(response => {
            this.props.updateItem(first_name, middle_name, last_name, hobby,birthday);
            this.props.handleClose();
        })
        .catch(function (error) {
            console.log(error);
        });
    };

    
    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.props.handleClose}
            />,
            <FlatButton
                label="Save"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSave}
            />,
        ];
        return (
            <div>
                <h2>Edit Profile</h2>
                <TextField
                    floatingLabelText="First Name:"
                    onChange={this.handleFirstName}
                    hintText='First Name'
                    defaultValue={this.state.first_name}
                    fullWidth={true}
                />
                <TextField
                    floatingLabelText="Middle Name:"
                    onChange={this.handleMiddleName}
                    hintText='Middle Name'
                    defaultValue={this.state.middle_name}
                    fullWidth={true}
                />
                <TextField
                    floatingLabelText="Last Name:"
                    onChange={this.handleLastName}
                    hintText='Last Name'
                    defaultValue={this.state.last_name}
                    fullWidth={true}

                />
                <TextField
                    floatingLabelText="Hobby:"
                    hintText='Hobby'
                    onChange={this.handleHobby}
                    fullWidth={true}
                    multiLine={true}
                    rowsMax={3}
                    defaultValue={this.state.hobby}
                />
                <DatePicker 
                    hintText="Birthday"
                    Dialog mode="landscape" 
                    openToYearSelection={true}
                    fullWidth={true}
                    onChange={this.handleBirthday}
                    defaultValue={this.state.birthday}

                />
                
                <FlatButton label="Save changes" onClick={this.handleSave}/>
            </div>
        );
    }
}

