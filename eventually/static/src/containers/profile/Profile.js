import React from 'react';
import ProfileEdit from './ProfileEdit';
import ProfileView from './ProfileView';
import {getUserId} from 'src/helper';
import {getProfileService} from './ProfileService';

export default class Profile extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            isEdit: false,
            isMyProfile: +this.props.match.params.profileId === getUserId(),
            id: '', 
            firstName: '',
            middleName: '',
            lastName: '',
            hobby: '',
            photo: '',
            birthday: new Date()    
        };
    }

    componentWillReceiveProps(nextProps){
        if (this.props.match.params.profileId !== nextProps.match.params.profileId) {
            this.getProfile(+nextProps.match.params.profileId);
        }
    }

    componentWillMount(){
        this.getProfile(+this.props.match.params.profileId);
    }


    getProfile = profileId => {
        getProfileService(profileId).then(response => {
            this.setState({
                id: response.data['user'],   
                isMyProfile: profileId === getUserId(),
                firstName: response.data['first_name'],
                middleName: response.data['middle_name'],
                lastName: response.data['last_name'],
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
        this.componentWillMount();
        this.setState({
            isEdit: false
        });
    };

    render(){

        const profileData = {
            id: this.state.id,
            firstName: this.state.firstName,
            middleName: this.state.middleName,
            lastName: this.state.lastName,
            hobby: this.state.hobby,
            photo: this.state.photo,
            birthday: this.state.birthday
        };

        const view = this.state.isEdit ? 
            (<ProfileEdit 
                profileData={profileData} 
                onCloseClick={this.handleClose}
            />) : 
            (<ProfileView
                profileData={profileData}
                isMyProfile={this.state.isMyProfile}
                onEditClick={this.handleEditClick}
            />);
        return(
            <div>
                {view}
            </div>
        );
    }
}
