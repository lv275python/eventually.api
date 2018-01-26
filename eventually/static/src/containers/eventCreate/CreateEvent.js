import React from 'react';
import axios from 'axios';
import { GetTeamsListService, PostEventService } from './CreateEventService';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import SelectField from 'material-ui/SelectField';



const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

class CreateEvent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            team: 0,
            description: '',
            status: 0,
            teams: [],
            open: false
        };
    }

     getData = () => {
         GetTeamsListService().then(response => {
             this.setState({teams: response.data.teams});
         });

     }

     componentWillMount() {
         this.getData();
     }

    handleChangeName = event => {
        this.setState({name: event.target.value});
    };

    handleChangeTeam = (event, index, value) => {
        this.setState({team: value});
    };

    handleChangeDescription = event => {
        this.setState({description: event.target.value});
    };

    handleChangeStatus = (event, index, value) => {
        this.setState({status: value});
    };

    handleSubmit = event => {
        event.preventDefault();

        const data = {
            'name': this.state.name,
            'team': this.state.team,
            'description': this.state.description,
            'status': this.state.status
        };
        PostEventService(data).then(response => {
            this.handleClose();
        });
    }

    handleOpen = () => {
        this.setState({ open: true });
    }

    handleClose = () => {
        this.setState({ open: false });
    }
    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSubmit}
            />,
        ];

        return (
            <div>
                <form>
                    <FloatingActionButton
                        onClick={this.handleOpen}
                        style={FlatButtonStyle}>
                        <ContentAdd />
                    </FloatingActionButton>
                    <Dialog
                        title={this.props.title}
                        actions={actions}
                        modal={false}
                        open={this.state.open}
                        onRequestClose={this.handleClose}>
                        <TextField
                            hintText="Name"
                            fullWidth={true}
                            value={this.state.name}
                            onChange={this.handleChangeName}/>
                        <TextField
                            value={this.state.description}
                            hintText="Description"
                            multiLine={true}
                            rows={2}
                            rowsMax={4}
                            fullWidth={true}
                            onChange={this.handleChangeDescription}/>
                        <SelectField
                            floatingLabelText="Team"
                            value={this.state.team}
                            onChange={this.handleChangeTeam}>
                            {
                                this.state.teams.map(team => {
                                    return <MenuItem value={team.id} key={team.id} primaryText={team.name} />;
                                }
                                )
                            }
                        </SelectField>
                        <SelectField
                            floatingLabelText="Status"
                            value={this.state.status}
                            onChange={this.handleChangeStatus}>
                            <MenuItem value={0} primaryText="draft" />
                            <MenuItem value={1} primaryText="published" />
                            <MenuItem value={2} primaryText="going" />
                            <MenuItem value={3} primaryText="finished" />
                        </SelectField>
                    </Dialog>
                </form>
            </div>
        );
    }
}

export default CreateEvent;
