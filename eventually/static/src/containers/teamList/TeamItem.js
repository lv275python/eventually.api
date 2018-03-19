import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import EditTeamDialog from './EditTeamDialog';
import {getImageUrl, getUserId} from 'src/helper';
import {teamServiceGet} from './teamService';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import Chip from 'material-ui/Chip';
import DeleteTeamDialog from './DeleteTeamDialog';

const styles = {
    container: {},
    team: {
        backgroundColor: 'rgba(208, 208, 208, 0.8)',
        borderRadius: 10,
        padding: 7,
    },
    header: {
        fontSize: '20px',
        fontWeight: 'bold',
        color: 'black',
    },
    description: {
        textAlign: 'justify',
    },
    members: {
        paddingTop: 20,
        float: 'left',
        width: '100%',
    },
    button: {
        float: 'right',
        marginTop: 10,
    },
    footer: {
        clear: 'both'
    },
    member: {
        marginTop: '1%',
        marginLeft: '2%',
    },
    list: {
        display: 'inline-block',
    }
};

export default class TeamItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: this.props.name,
            description: this.props.description.slice(0, 50) + '...',
            image: this.props.image,
            members:this.props.members,/*count of members*/
            listOfMembers:this.props.listOfMembers,/*list with id of members*/
            listOfNamesMembers:[],
            open: false,
            openDel: false,
            teamDeleted: false,
            owner: this.props.owner,
            expanded: false,
        };
    }

    /*open dialog for editing*/
    handleOpen = () => {
        this.setState({open: true});
    };
    /*close dialog for editing*/
    handleClose = () => {
        this.setState({open: false});
    };
    /*expand card*/
    handleExpandChange = (expanded) => {
        this.setState({expanded: expanded});
        if (this.state.expanded == false) {
            this.setState({
                description: this.props.description,
                open_more: !this.state.expanded
            });
        } else {
            this.setState({
                description: this.props.description.slice(0, 50) + '...',
                open_more: !this.state.expanded
            });
        }
    };
    /*update old prop*/
    componentWillReceiveProps(nextProps) {
        this.setState({
            name: nextProps.name,
            description: nextProps.description.slice(0, 50) + '...',
            image: nextProps.image,
        });
    }
    /*open dialog for deleting*/
    handleOpenDel = () => {
        this.setState({openDel: true});
    };
    /*close dialog for deleting*/
    handleCloseDel = () => {
        this.setState({openDel: false});
    };
    /*checks if user is owner of team*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
            return true;
        } else {
            return false;
        }
    };
    /*changes state when team is deleted*/
    confirmDeleteTeam = () => {
        this.setState({teamDeleted: true});
    };

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
        if (this.ownerCheck() == true) {
            delButton = <RaisedButton
                label="Delete"
                style={styles.button}
                backgroundColor="#D50000"
                labelColor="#FFF"
                onClick={this.handleOpenDel}
            />;
        } else {
            delButton = '';
        }

        let teamView;
        if (this.state.teamDeleted == false) {
            teamView = (
                <div>
                    <Card style={styles.team} expanded={this.state.expanded} onExpandChange={this.handleExpandChange}>
                        <CardHeader title={this.state.name}
                            actAsExpander={true}
                            showExpandableButton={true}
                            style={styles.header}/>
                        <CardText>
                            <div style={styles.description}>{this.state.description}</div>
                            <div style={styles.members}>Members:<span>{this.props.members}</span></div>
                        </CardText>
                        <CardText expandable={true} style={styles.list}>
                            {
                                this.state.listOfMembers.map(usr => (
                                    <div key={usr['id']} style={styles.member}>
                                        <Chip onClick={() => this.props.goToUserProfile(usr['id'])}>
                                            <Avatar src={(usr['photo']) && getImageUrl(usr['photo'])}/>
                                            {usr['first_name'] + '  ' + usr['last_name']}
                                        </Chip>
                                    </div>
                                ))
                            }
                        </CardText>
                        <RaisedButton label="Edit" onClick={this.handleOpen} style={styles.button}/>
                        {delButton}
                        <div style={styles.footer}></div>
                        <EditTeamDialog
                            open={this.state.open}
                            handleClose={this.handleClose}
                            name={this.props.name}
                            description={this.props.description}
                            image={this.props.image}
                            updateItem={this.props.updateItem}
                            id={this.props.id}
                        />
                    </Card>
                </div>
            );
        } else {
            teamView = (
                <div style={styles.team}>
                    <p>Team '{this.state.name}' successfully deleted</p>
                </div>
            );
        }

        return (
            <div>
                <div style={styles.container}>
                    {teamView}
                    <div style={styles.footer}></div>
                </div>
                <EditTeamDialog
                    open={this.state.open}
                    handleClose={this.handleClose}
                    name={this.props.name}
                    description={this.props.description}
                    image={this.props.image}
                    updateItem={this.props.updateItem}
                    id={this.props.id}
                />
                <DeleteTeamDialog
                    openDel={this.state.openDel}
                    handleCloseDel={this.handleCloseDel}
                    name={this.props.name}
                    description={this.props.description}
                    id={this.props.id}
                    confirmDeleteTeam={this.confirmDeleteTeam}
                />
            </div>
        );
    }
}
