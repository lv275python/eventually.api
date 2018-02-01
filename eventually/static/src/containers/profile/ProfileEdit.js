import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import DatePicker from 'material-ui/DatePicker';
import {Card, CardHeader} from 'material-ui/Card';
import {putProfileService, getProfileService} from './ProfileService';
import {getImageUrl} from './helper';
import {FileUpload} from './containers';

const style_card = {
    display: 'flex',
    justifyContent: 'center',
};

const style_name = {
    margin: '10px 100px 0 100px',
    height: '400px',
    width: '400px',
};

const style_main_div = {
    display: 'flex',
    justifyContent: 'center',
};
const style_title = {      
    fontSize: '35px',     
};

const style_header = {        
    display: 'flex',      
    alignItems: 'center',     
    justifyContent: 'center',     
};

const style_buttons = {        
    display: 'flex',      
    alignItems: 'flex-end',     
    justifyContent: 'space-around',    
    margin: '20px 20px 40px 350px' , 
    width: '40%',
};

const style_container = {
    width: '150px',
    height: '150px',
    margin:'0px 100px',
};


export default class ProfileEdit extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={style_main_div}>
                <Card style={style_card}>
                    <CardHeader style = {style_header}      
                        title="Edit profile"      
                        titleStyle={style_title}        
                    />
                    <div style={style_name}>
                        <TextField
                            floatingLabelText="First Name:"
                            onChange={this.props.onFirstNameChange}
                            hintText='First Name'
                            value={this.props.profileData.first_name}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Middle Name:"
                            onChange={this.props.onMiddleNameChange}
                            hintText='Middle Name'
                            value={this.props.profileData.middle_name}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Last Name:"
                            onChange={this.props.onLastNameChange}
                            hintText='Last Name'
                            value={this.props.profileData.last_name}
                            fullWidth={true}
                        />
                        <TextField
                            floatingLabelText="Hobby:"
                            hintText='Hobby'
                            onChange={this.props.onHobbyChange}
                            fullWidth={true}
                            multiLine={true}
                            rowsMax={3}
                            value={this.props.profileData.hobby}
                        />
                        <DatePicker 
                            floatingLabelText="Birthday:"
                            hintText="Birthday"
                            mode="landscape"
                            openToYearSelection={true}
                            fullWidth={true}
                            onChange={this.props.onBirthdayChange}
                            value={this.props.profileData.birthday}
                        />
                    </div>
                    <div style={style_container}>
                        <img src={this.props.profileData.photo && getImageUrl(this.props.profileData.photo)}
                            alt=""
                            style={{maxHeight: '100%'}}
                        />
                        <FileUpload 
                            updateImageNameInDb={this.props.uploadImage}
                        />
                    </div>
                        
                    <div style={style_buttons}>
                        <RaisedButton
                            label="Cancel"
                            secondary={true}
                            keyboardFocused={true}
                            onClick={this.props.onCloseClick}
                        />
                        <RaisedButton
                            label="Save"
                            primary={true}
                            keyboardFocused={true}
                            onClick={this.props.onSaveClick}
                        />
                    </div>
                </Card>
            </div>
        );
    }
}
