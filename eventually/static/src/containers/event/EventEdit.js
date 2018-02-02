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


const dateStyle = {
    display: 'inline-block',
    width: '50%'
};

export default class EventEdit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.id,
            teams: [],
            open: false,
            teamId: this.props.team,
            owner: this.props.owner,
            name: this.props.name,
            description: this.props.description,
            start_at: this.props.start_at,
            duration: this.props.duration,
            budget: this.props.budget,
            status: this.props.status,
        };
    }

    componentWillMount(){
        this.getTeamItem();
    }

    getTeamItem = () => {
        teamServiceGet().then(response => {
            this.setState({
                teams: response.data.teams
            });
        });
    };

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

    handleDuration = (event,date) => {
        this.setState({duration:(date/1000)-this.state.start_at});
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
        const duration = this.state.duration;

        putEventService( this.state.eventId, teamId, name, description, start_at, budget, status, duration);
        this.handleClose();
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
            <div>
                <form>

                    <RaisedButton
                        label="Edit"
                        primary={true}
                        keyboardFocused={true}
                        onClick={this.handleOpen}
                    />

                    <Dialog
                        title={this.props.title}
                        actions={actions}
                        modal={false}
                        open={this.state.open}
                        onRequestClose={this.handleClose}
                        autoScrollBodyContent={true}
                    >

                        <TextField
                            floatingLabelText="Name:"
                            onChange={this.handleName}
                            hintText='Name'
                            value={this.state.name}
                            fullWidth={true}
                        />

                        <TextField
                            floatingLabelText="Description:"
                            onChange={this.handleDescription}
                            hintText='Description'
                            value={this.state.description}
                            fullWidth={true}
                        />

                        <DatePicker
                            floatingLabelText="Start date and time."
                            onChange={this.handleStartAt}
                            mode="landscape"
                            style={dateStyle}
                            fullWidth={true}
                            value={new Date(this.state.start_at*1000)}
                        />

                        <TimePicker
                            textFieldStyle={{width: '100%'}}
                            format="24hr"
                            hintText="24hr Format"
                            style={dateStyle}
                            value={new Date(this.state.start_at*1000)}
                            onChange={this.handleStartAt}
                        />

                        <DatePicker
                            floatingLabelText="End date and time."
                            onChange={this.handleDuration}
                            mode="landscape"
                            style={dateStyle}
                            fullWidth={true}
                            value={new Date((this.state.start_at+this.state.duration)*1000)}
                        />

                        <TimePicker
                            textFieldStyle={{width: '100%'}}
                            format="24hr"
                            hintText="24hr Format"
                            style={dateStyle}
                            value={new Date((this.state.start_at+this.state.duration)*1000)}
                            onChange={this.handleDuration}
                        />

                        <SelectField
                            floatingLabelText="Team:"
                            hintText="Team"
                            fullWidth={true}
                            value = {this.state.teamId}
                            onChange={this.handleTeams}
                        >
                            {this.state.teams.map(teams => {
                                return <MenuItem key={teams.id}  value = {teams.id} primaryText = {teams.name} />;
                            })}
                        </SelectField>

                        <TextField
                            floatingLabelText="Budget:"
                            onChange={this.handleBudget}
                            hintText='Budget'
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
                    </Dialog>
                </form>
            </div>

        );
    }
}
