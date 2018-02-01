import React from 'react';
import ProfileEdit from './ProfileEdit';
import ProfileView from './ProfileView';
import {getUserId} from './helper';
import {getProfileService, putProfileService} from './ProfileService';

export default class Profile extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isEdit: false,
            isMyProfile: +this.props.match.params.profileId === getUserId(),
            id: '', 
            first_name: '',
            middle_name: '', 
            last_name: '',
            hobby: '',
            photo: '',
            birthday: new Date()    
        };
    }

    componentWillMount(){
        this.getProfile(+this.props.match.params.profileId);
    }

    getProfile = (profileId) => {
        getProfileService(profileId).then(response => {
            this.setState({
                id: response.data['user'],   
                first_name: response.data['first_name'],
                middle_name: response.data['middle_name'], 
                last_name: response.data['last_name'],
                hobby: response.data['hobby'],
                photo: response.data['photo'],
                birthday: new Date(response.data['birthday'])
            });
        });                 
    }


    handleEditClick = () => {
        this.setState({
            isEdit: true
        });
    }

    handleClose = () => {
        this.setState({
            isEdit: false
        });
    }

    handleFirstNameChange = event => {
        this.setState({
            first_name: event.target.value
        });
    };

    handleMiddleNameChange = event => {
        this.setState({
            middle_name: event.target.value
        });
    };

    handleLastNameChange = event => {
        this.setState({
            last_name: event.target.value
        });
    };

    handleHobbyChange = event => {
        this.setState({
            hobby: event.target.value
        });
    };

    handleBirthdayChange = (event, date) => {
        this.setState({
            birthday: date
        });
    };

    uploadImage = imageName => {
        this.setState({photo: imageName});
    }

    handleSave = () => {
        const first_name = this.state.first_name;
        const middle_name = this.state.middle_name;
        const last_name = this.state.last_name;
        const hobby = this.state.hobby;
        const photo = this.state.photo;
        const birthday = this.state.birthday.getFullYear() + '-' +(this.state.birthday.getMonth() + 1) + '-' +  this.state.birthday.getDate();
        

        putProfileService(this.state.id, first_name, middle_name, last_name, hobby, photo, birthday)
            .then(response => {
                this.handleClose();
            });
    };

    
    render(){

        const profileData = {
            id: this.state.id,
            first_name: this.state.first_name,
            middle_name: this.state.middle_name,
            last_name: this.state.last_name,
            hobby: this.state.hobby,
            photo: this.state.photo,
            birthday: this.state.birthday
        };

        const view = this.state.isEdit ? 
            (<ProfileEdit 
                profileData={profileData} 
                onCloseClick={this.handleClose}
                onEditClick={this.handleEditClick} 
                onFirstNameChange={this.handleFirstNameChange} 
                onMiddleNameChange={this.handleMiddleNameChange} 
                onLastNameChange={this.handleLastNameChange} 
                onHobbyChange={this.handleHobbyChange} 
                onBirthdayChange={this.handleBirthdayChange}
                uploadImage={this.uploadImage}
                onSaveClick={this.handleSave} 
            />) : 
            (<ProfileView profileData={profileData} isMyProfile={this.state.isMyProfile} onEditClick={this.handleEditClick} />);
        return(
            <div>
                {view}
            </div>
        );
    }
}
