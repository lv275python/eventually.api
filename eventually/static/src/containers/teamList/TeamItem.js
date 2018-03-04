import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Subheader from 'material-ui/Subheader';
import EditTeamDialog from './EditTeamDialog';
import {getImageUrl, getUserId} from 'src/helper';
import {teamServiceGet, teamServiceDelete} from './teamService';


const styles = {
    container: {},
    team: {
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
    members: {
        paddingTop: 20,
        float: 'left',
    },
    button: {
        float: 'right',
        marginTop: 10,
    },
    footer: {
        clear: 'both'
    },
};

export default class TeamItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            description: this.props.description.slice(0,300)+'...',
            image: this.props.image,
            members: this.props.members,/*count of members*/
            listOfMembers: this.props.listOfMembers,/*list with id of members*/
            listOfNamesMembers: [],
            open: false,
            open_more:false,
            id: this.props.id,
            owner: this.props.owner,
            stateOfTeamView: 0
        };
    }
    /*update old prop*/
    componentWillReceiveProps(nextProps){
        this.setState({
            name: nextProps.name,
            description: nextProps.description.slice(0,300)+'...',
            image: nextProps.image,
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
    /*button `More info`*/
    handleToggle = () => {
        if (this.state.open_more == false){
            this.setState({
                description: this.props.description,
                open_more: !this.state.open_more
            });
        }else{
            this.setState({
                description: this.props.description.slice(0,300)+'...',
                open_more: !this.state.open_more
            });
        }
    }
    /*check if user is author of team*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
            return true;
        } else {
            return false;
        }
    }
    /*changes state of 'stateOfTeamView' field to display delete team offer */
    offerDelete = () => {
        this.setState({stateOfTeamView: 1});
    }
    /*changes state of 'stateOfTeamView' field to return to team view*/
    cancelDelete = () => {
        this.setState({stateOfTeamView: 0});
    }
    /*deletes team and changes state 'stateOfTeamView'*/
    deleteTeam = () => {
        teamServiceDelete(this.state.id).then(response => {
            if (response.status == 200) {
                this.setState({stateOfTeamView: 2});
            } else if (response.status == 404) {
                this.setState({stateOfTeamView: 3});
            } else {
                this.setState({stateOfTeamView: 4});
            }
        });
    }

    render() {
        styles.container = {
            'background': 'url(' + getImageUrl(this.state.image) + ')',
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
        };

        let delButton;
        if (this.ownerCheck()==true) {
            delButton = <RaisedButton
                label="Delete" 
                secondary={true} 
                style={styles.button}
                onClick={this.offerDelete}
            />;
        } else{
            delButton = '';
        }

        let teamView;
        if (this.state.stateOfTeamView==0) {
            teamView = (
                <div style={styles.team}>
                    <Subheader style={styles.header}>{this.state.name}</Subheader>
                    <div style={styles.description}>{this.state.description}</div>
                    <div style={styles.members}>Members:<span>{this.props.members}</span></div>
                    {delButton}
                    <RaisedButton
                        label="Edit"
                        primary={true}
                        onClick={this.handleOpen}
                        style={styles.button}
                    />
                    <RaisedButton
                        label="More info"
                        onClick={this.handleToggle}
                        style={styles.button}
                    />
                    <div style={styles.footer}></div>
                </div>
            );
        } else if (this.state.stateOfTeamView==1) {
            teamView = (
                <div style={styles.team}>
                    <p>Are you sure you want to delete team '{this.state.name}'?</p>
                    <RaisedButton
                        label="Cancel"
                        onClick={this.cancelDelete}
                        primary={true}
                        style={styles.button}
                    />
                    <RaisedButton
                        label="Delete completely"
                        onClick={this.deleteTeam}
                        secondary={true}
                        style={styles.button}
                    />
                    <div style={styles.footer}></div>
                </div>
            );
        } else if (this.state.stateOfTeamView==2) {
            teamView = <p>Team '{this.state.name}' successfully deleted</p>;
        } else if (this.state.stateOfTeamView==3) {
            teamView = <p>Team '{this.state.name}' was not found. Probably, somebody already deleted it. Please, reload page.</p>;
        } else if (this.state.stateOfTeamView==4) {
            teamView = <p>Unknown error. Reload page and try again.</p>;
        }

        return (
            <div style={styles.container}>
                {teamView}
                <EditTeamDialog
                    open = {this.state.open}
                    handleClose = {this.handleClose}
                    name = {this.props.name}
                    description = {this.props.description}
                    image = {this.props.image}
                    updateItem = {this.props.updateItem}
                    id = {this.props.id}
                />
            </div>
        );
    }
}
