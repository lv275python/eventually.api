import React from 'react';
import {putProfileService} from './ProfileService.js';

import TextField from 'material-ui/TextField';
import FlatButton from 'material-ui/FlatButton'


export default class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);;
        this.state = {};
    };
    
    handleHobby = event => {
        this.setState({hobby: event.target.value});

    }

    handleFirstName = event => {
        this.setState({first_name: event.target.value});

    }
    
    handleSave = event => {
        const hobby = this.state.hobby;
        const first_name = this.state.first_name
        putUserService(first_name)
            .then((response) => {
                this.props.history.push('/profile');
            });
        putProfileService(hobby)
            .then((response) => {
                this.props.history.push('/profile');
            });
        event.preventDefault();
    };

    render() {
        return (
            <div>
                <h2>Edit Profile</h2>
                <TextField
                    floatingLabelText="Hobby:"
                    onChange={this.handleHobby}
                    hintText='Hobby'
                /><br/>
                <TextField
                    floatingLabelText="Name:"
                    onChange={this.handleFirstName}
                    hintText='First Name'
                /><br/>
                <FlatButton label="Save changes" onClick={this.handleSave}/>
            </div>
        );
    }
}

