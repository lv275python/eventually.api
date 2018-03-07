import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Subheader from 'material-ui/Subheader';
import EditTeamDialog from './EditTeamDialog';
import {getImageUrl, getUserId} from 'src/helper';
import {teamServiceGet} from './teamService';
import DeleteTeamDialog from './DeleteTeamDialog';

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
            members:this.props.members,/*count of members*/
            listOfMembers:this.props.listOfMembers,/*list with id of members*/
            listOfNamesMembers:[],
            open: false,
            open_more:false,
            openDel: false,
            teamDeleted: false,
            owner: this.props.owner
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
    /*open dialog for deleting*/
    handleOpenDel = () => {
        this.setState({openDel: true});
    };
    /*close dialog for deleting*/
    handleCloseDel = () => {
        this.setState({openDel: false});
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
    /*checks if user is owner of team*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
            return true;
        } else {
            return false;
        }
    }
    /*changes state when team is deleted*/
    comfirmDeleteTeam = () => {
        this.setState({teamDeleted: true});
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
                style={styles.button}
                backgroundColor="#D50000"
                labelColor="#FFF"
                onClick={this.handleOpenDel}
            />;
        } else{
            delButton = '';
        }

        let teamView;
        if (this.state.teamDeleted==false) {
            teamView = (
                <div>
                    <Subheader style={styles.header}>{this.state.name}</Subheader>  
                    <div style={styles.description}>{this.state.description}</div>
                    <div style={styles.members}>Members:<span>{this.props.members}</span></div>
                    <RaisedButton label="More info" primary={true} onClick={this.handleToggle} style={styles.button}/>
                    <RaisedButton label="Edit" onClick={this.handleOpen} style={styles.button}/>
                    {delButton}
                </div>
            );
        } else {
            teamView = <p>Team '{this.state.name}' successfully deleted</p>;
        }

        return (
            <div style={styles.container}>
                <div style={styles.team}>
                    {teamView}
                    <div style={styles.footer}></div>
                </div>
                <EditTeamDialog
                    open = {this.state.open}
                    handleClose = {this.handleClose}
                    name = {this.props.name}
                    description = {this.props.description}
                    image = {this.props.image}
                    updateItem = {this.props.updateItem}
                    id = {this.props.id}
                />
                <DeleteTeamDialog
                    openDel = {this.state.openDel}
                    handleCloseDel = {this.handleCloseDel}
                    name = {this.props.name}
                    description = {this.props.description}
                    id = {this.props.id}
                    comfirmDeleteTeam = {this.comfirmDeleteTeam}
                />
            </div>
        );
    }
}
