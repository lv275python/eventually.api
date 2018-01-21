import React from 'react';
import {Card, CardActions, CardHeader, CardMedia, CardTitle, CardText} from 'material-ui/Card';
import {getEventService, putEventService} from './EventService.js';
import {teamServiceGet} from '../teamList/teamService.js';

import DatePicker from 'material-ui/DatePicker';
import TimePicker from 'material-ui/TimePicker';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';

const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%',
};


const style_main_div = {
    display: 'flex',
    justifyContent: 'center',
};

const style_card = {
    display: 'flex',
    justifyContent: 'center',
};

const style_name = {
    margin: '10px 100px 0 100px',
    height: '700px',
    width: '400px',
};

const style_header = {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
};

const style_title = {
    fontSize: '35px',
};

const date_style = {
    width: '350px',
    display: 'inline-block',
};

const time_style = {
    width: '50px',
    display: 'inline-block',
};


export default class EventEdit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.eventId,
            teamId: this.props.teamId,
            name: '',
            description: '',
            start_at: '',
            budget: '',
            status: '',
            teams: [],
            open: false,
        };
    }

    componentWillMount(){
        this.getItem();
        this.getTeamItem();

    }

    getTeamItem = () => {
        teamServiceGet().then(response => {
            this.setState({
                teams: response.data.teams
            });
        });

    };



    getItem = () => {
        getEventService(this.state.eventId).then(response => {
            this.setState({
                name: response.data['name'],
                description: response.data['description'],
                start_at: response.data['start_at'],
                budget: response.data['budget'] ? response.data['budget'] : '' ,
                status: response.data['status']
            });
        });
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    handleTeams = (event, index, teams) => this.setState({teamId : teams});


    handleName = event => {
        this.setState({name: event.target.value});
    };

    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    handleStartAt = (event,date) => {
        this.setState({start_at:date/1000});
    };

    handleBudget = event => {
        this.setState({budget: event.target.value});
    };

    handleStatus = (event, index, status) => this.setState({status});


    handleSave = () => {
        const teamId = this.state.teamId;
        const name = this.state.name;
        const description = this.state.description;
        const start_at = this.state.start_at;
        const budget = this.state.budget;
        const status = this.state.status;

        putEventService( this.state.eventId, teamId, name, description, start_at, budget, status)
            .then(response => {
                console.log(response);
            })
            .catch(function (error) {
                console.log(error);
            });

    }

    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Save"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleSave}
            />,
        ];
        return (
            <div style={style_main_div}>

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
                    onRequestClose={this.handleClose}
                >

                    <div style={style_name}>

                        <TextField
                            floatingLabelText="Name:"
                            onChange={this.handleName}
                            hintText='Name'
                            value={this.state.name}
                            fullWidth={true}
                        />

                        <SelectField
                            floatingLabelText="Teams:"
                            hintText="Teams"
                            fullWidth={true}
                            value = {this.state.teamId}
                            onChange={this.handleTeams}
                        >
                            {this.state.teams.map(teams => {
                                return <MenuItem key={teams.id}  value = {teams.id} primaryText = {teams.name} />;
                            })}
                        </SelectField>


                        <TextField
                            floatingLabelText="Description:"
                            onChange={this.handleDescription}
                            hintText='Description'
                            value={this.state.description}
                            fullWidth={true}
                        />

                        <div style = {date_style}>
                            <DatePicker
                                floatingLabelText="The date and time the event will occur."
                                onChange={this.handleStartAt}
                                mode="landscape"
                                fullWidth={true}
                                value={new Date(this.state.start_at*1000)}
                            />
                        </div>
                        <div style = {time_style}>
                            <TimePicker
                                textFieldStyle={{width: '100%'}}
                                format="24hr"
                                hintText="24hr Format"
                                value={new Date(this.state.start_at*1000)}
                                onChange={this.handleStartAt}
                            />

                        </div>
                        <TextField
                            floatingLabelText="Budget:"
                            onChange={this.handleBudget}
                            hintText='Budget in hryvnias'
                            value={this.state.budget}
                            fullWidth={true}
                        />

                        <SelectField
                            floatingLabelText="Status"
                            value={this.state.status}
                            onChange={this.handleStatus}
                        >
                            <MenuItem value={0} primaryText="Draft" />
                            <MenuItem value={1} primaryText="Published" />
                            <MenuItem value={2} primaryText="Going" />
                            <MenuItem value={3} primaryText="Finished" />
                        </SelectField>
                    </div>
                </Dialog>
            </div>

        );
    }
}


