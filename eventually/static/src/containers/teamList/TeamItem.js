import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Subheader from 'material-ui/Subheader';
import EditTeamDialog from './EditTeamDialog';
import {getImageUrl} from '../../helper';
import {teamServiceGet} from './teamService';

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
            open_more:false
        };
    }
    /*update old prop*/
    componentWillReceiveProps (nextProps){
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

        return (
            <div style={styles.container}>
                <div style={styles.team}>
                    <Subheader style={styles.header}>{this.state.name}</Subheader>
                    <div style={styles.description}>{this.state.description}</div>
                    <div style={styles.members}>Members:<span>{this.props.members}</span></div>
                    <RaisedButton label="More info" primary={true} onClick={this.handleToggle} style={styles.button}/>
                    <RaisedButton label="Edit" onClick={this.handleOpen} style={styles.button}/>
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
            </div>
        );
    }
}
