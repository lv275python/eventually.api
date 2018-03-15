import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Subheader from 'material-ui/Subheader';
import SuggestedTopicsEdit from './SuggestedTopicsEdit';
import InterestedUsersChips from './InterestedUsersChips';
import {getUserId} from 'src/helper';
import Chip from 'material-ui/Chip';
import {getProfileService} from 'src/containers';
import {putSuggestedTopicsItem} from './SuggestedTopicsService';



const styles = {
    container: {
            'backgroundRepeat': 'no-repeat',
            'backgroundPosition': 'center',
            'backgroundSize': 'cover',
            'borderRadius': 10,
            'borderWidth': 1,
            'borderColor': 'black',
            'borderStyle': 'solid',
            'padding': 15,
            'width': '90%',
            'margin': '0 auto',
            'marginTop': 37
        },
    topics: {
        backgroundColor: 'rgba(208, 208, 208, 0.8)',
        borderRadius: 10,
        padding: 7,
    },
    header: {
        fontSize: '21px',
        color: 'black',
    },
    description: {
        textAlign: 'justify',
    },
    button: {
        float: 'right',
        marginTop: 10,
    },
    footer: {
        clear: 'both'
    },
    chip: {
        margin: 4,
    },
    wrapper: {
        display: 'flex',
        flexWrap: 'wrap',
    },
};


export default class SuggestedTopicsItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open : false,
            name: this.props.name,
            description: this.props.description,
            owner: this.props.owner,
            interestedUsers: this.props.interestedUsers,
            usersDetails: [],
            removeInterest: '',
            joinButtonLabel: '',
        };
    }

    componentWillMount(){
        this.getInterestedUsersDetails();
        this.handleUserInTopic();
    }

    handleUserInTopic = () => {
        if (this.state.interestedUsers.indexOf(getUserId()) === -1){
            this.setState({joinButtonLabel: 'Join'})
            this.setState({removeInterest: '0'})
        } else {
            this.setState({joinButtonLabel: 'Leave'})
            this.setState({removeInterest: '1'})
        }
    };

    /*update old prop*/
    componentWillReceiveProps(nextProps){
        this.setState({
            name: nextProps.name,
            description: nextProps.description,
        });
    }

     /*open dialog for editing*/
    handleOpen = () => {
        this.setState({open: true});
    };

    /*close dialog for editing*/
    handleClose = () => {
        this.setState({open: false});
    };

    /*check if user is author of suggested topic*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
           return true;
        } else {
            return false;
        }
    };

    getInterestedUsersDetails = () =>{
        const users = this.props.interestedUsers;
        users.map(userId => (
            getProfileService(userId).then(response => {
                let usersDetails = this.state.usersDetails;
                usersDetails.push(response.data);
                this.setState(usersDetails);
            })
        ))
    }

    switchJoinButton = () => {
        if (this.state.removeInterest === '0'){
            this.setState({joinButtonLabel: 'Leave'})
            this.setState({removeInterest: '1'})
        } else {
            this.setState({joinButtonLabel: 'Join'})
            this.setState({removeInterest: '0'})
        }    
        console.log(this.state.usersDetails)
        this.handleInterested()
    }


    handleInterested = () => {
        const id = this.props.id;
        const name = this.state.name;
        const description = this.state.description;
        const interestedUser = getUserId();
        const removeInterest = this.state.removeInterest;
        putSuggestedTopicsItem(id, name, description, interestedUser, removeInterest);
    }

    render() {

        let editButton;
        if (this.ownerCheck()==true) {
            editButton = <RaisedButton
            label='Edit'
            secondary={true}
            style={styles.button}
            onClick={this.handleOpen}
        />;
        }else{
            editButton = '';
        }

        return (
            <div style={styles.container}>
                <div style={styles.topics}>
                    <Subheader style={styles.header}> {this.state.name} </Subheader>
                    <div style={styles.description}> {this.state.description} </div>
                    {editButton}
                    <RaisedButton
                        onClick={this.switchJoinButton}
                        label={this.state.joinButtonLabel}
                        primary={true}
                        style={styles.button}
                    />
                    <div style={styles.wrapper}>
                        {this.state.usersDetails.map( involved => (
                            <InterestedUsersChips
                                id={involved['id']}
                                key={involved['user']}
                                text={involved['first_name'] + ' ' + involved['last_name']} />
                        ))}
                    </div>
                    <div style={styles.footer}></div>
                </div>

                <SuggestedTopicsEdit
                    id = {this.props.id}
                    name = {this.props.name}
                    description = {this.props.description}
                    updateTopic = {this.props.updateTopic}
                    open = {this.state.open}
                    handleClose = {this.handleClose}
                />
            </div>
        );
    }
}
