import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {teamServiceDelete} from './teamService';
import {redA700, orange500} from 'material-ui/styles/colors';


const errorStyle = {
    color: orange500,
};

export default class DeleteTeamDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            id: this.props.id,
            name: this.props.name,
            description: this.props.description,
            responseError: false
        };
    }
    /*handles errors on deleting team status and closing dialog if success*/
    deleteTeam = () => {
        teamServiceDelete(this.state.id).then(response => {
            if (response.status == 200) {
                this.props.comfirmDeleteTeam();
                this.props.handleCloseDel();
            } else {
                this.setState({responseError: response.status});
            }
        });
    }
    /*closes delete dialog and resets responseError state*/
    closeDialog = () => {
        this.setState({responseError: false});
        this.props.handleCloseDel();
    };

    render() {
        const actions = [
            <RaisedButton
                backgroundColor={redA700}
                labelColor="#FFF"
                label="Yes"
                onClick={this.deleteTeam}
            />,
            <FlatButton
                label="No"
                primary={true}
                onClick={this.closeDialog}
            />
        ];

        return (
            <Dialog
                title={'Remove team "' + this.state.name + '" completely?'}
                actions={actions}
                modal={false}
                autoDetectWindowHeight={true}
                onRequestClose={this.closeDialog}
                open={this.props.openDel}
            >
                {(this.state.description!='')?
                    <p>Description: {this.state.description}</p>
                    :'Team has no description'}
                {(this.state.responseError!=false)?
                    <p style={errorStyle}>Attemp to delete team failed. Error status: {this.state.responseError}</p>
                    : ''}
            </Dialog>
        );
    }
}
