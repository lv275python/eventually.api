import React from 'react';
import axios from 'axios';
import Location from './GoogleLocation';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import MenuItem from 'material-ui/MenuItem';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import SelectField from 'material-ui/SelectField';
import DatePicker from 'material-ui/DatePicker';
import TimePicker from 'material-ui/TimePicker';
import Snackbar from 'material-ui/Snackbar';
import { CancelDialog } from 'src/containers';
import { getTeamsListService, postEventService } from './EventService';


const FlatButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

const dateStyle = {
    display: 'inline-block',
    width: '50%'
};

class CreateEvent extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            failNameMessage: '',
            failDescriptionMessage: '',
            failBudgetMessage: '',
            nameIsValid: false,
            descriptionIsValid: false,
            budgetIsValid: true,
            name: '',
            team: null,
            description: '',
            startAt: new Date() / 1000,
            timeEnd: new Date() / 1000,
            budget: 0,
            status: 0,
            teams: [],
            formattedAddress: '',
            longitude: 0,
            latitude: 0,
            open: false,
            openCancelDialog: false,
            responseError: ''
        };
    }

    getData = () => {
        getTeamsListService().then(response => {
            this.setState({ teams: response.data.teams });
        });
    }

    componentWillMount() {
        this.getData();
    }

    handleChangeName = event => {
        const regex = /^.{4,64}$/;
        if(regex.test(event.target.value) === true) {
            this.setState({
                failNameMessage: '',
                nameIsValid: true,
                name: event.target.value
            });
        } else {
            this.setState({
                nameIsValid: false,
                failNameMessage: 'Name must be greater than 4 and less 64 any symbols'
            });
        }
    };

    handleChangeStartAt = (event, date) => {
        this.setState({
            startAt: date / 1000,
            timeEnd: date / 1000
        });
    };

    handleChangeTimeEnd = (event, date) => {
        this.setState({ timeEnd: date / 1000 });
    };

    handleChangeBudget = event => {
        const regex = /^[0-9]{0,6}$/;
        if(regex.test(event.target.value) === true) {
            this.setState({
                failBudgetMessage: '',
                budget: event.target.value
            });
        } else {
            this.setState({
                budgetIsValid: false,
                failBudgetMessage: 'Value must be a number and maximum be less 1000000'
            });
        }
    };

    handleChangeLocation = value => {
        this.setState({
            formattedAddress: value.formattedAddress,
            longitude: value.location.lng,
            latitude: value.location.lat,
        });
    };

    handleChangeTeam = (event, index, value) => {
        this.setState({ team: value });
    };

    handleChangeDescription = event => {
        const regex = /^[\S\s.]{0,1024}$/;
        if(regex.test(event.target.value) === true) {
            this.setState({
                failDescriptionMessage: '',
                descriptionIsValid: true,
                description: event.target.value
            });
        } else {
            this.setState({
                failDescriptionMessage: 'Description must be less 1024 any symbols'
            });
        }
    };

    handleChangeStatus = (event, index, value) => {
        this.setState({ status: value });
    };

    openErrorSnackBar = () => {
        this.setState({
            openErrorSnackBar: true,
        });
    };

    closeErrorSnackBar = () => {
        this.setState({
            openErrorSnackBar: false,
        });
    };

    handleSubmit = event => {
        event.preventDefault();
        const data = {
            'name': this.state.name,
            'description': this.state.description,
            'start_at': this.state.startAt,
            'duration': this.state.timeEnd - this.state.startAt,
            'budget': Number(this.state.budget),
            'team': this.state.team,
            'status': this.state.status,
            'longitude': this.state.longitude,
            'latitude': this.state.latitude
        };
        postEventService(data).then(
            response => {
                this.props.addEvent(response.data);
                this.handleClose();
            },
            error => {
                this.setState({responseError: error.response.data[0].toUpperCase() + error.response.data.slice(1)});
                this.openErrorSnackBar();
            }
        );
    };

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState({ open: false });
        this.setState({
            name: '',
            team: null,
            description: '',
            startAt: new Date() / 1000,
            timeEnd: new Date() / 1000,
            budget: 0,
            status: 0,
            formattedAddress: '',
            failNameMessage: '',
            failDescriptionMessage: '',
            failBudgetMessage: '',
            nameIsValid: false,
            descriptionIsValid: false,
            budgetIsValid: true
        });
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelCreateDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.team != null) ||
            (this.state.name != '') ||
            (this.state.description != '') ||
            (this.state.budget != 0) ||
            (this.state.status != 0)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleClose();
    };

    render() {
        let submitButtonDisabled = !(
            this.state.nameIsValid && this.state.descriptionIsValid && this.state.budgetIsValid &&
            this.state.team !== null && (this.state.timeEnd - this.state.startAt) > 0 &&
            this.state.formattedAddress !==''
        );

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
                disabled={submitButtonDisabled}
                onClick={this.handleSubmit}
            />,
        ];

        return (
            <div>
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
                    onRequestClose={this.handleRequestClose}
                    autoScrollBodyContent={true}
                    style={{zIndex: 800}}>
                    <TextField
                        hintText="Name"
                        fullWidth={true}
                        defaultValue={this.state.name}
                        errorText={this.state.failNameMessage}
                        onChange={this.handleChangeName}/>
                    <TextField
                        defaultValue={this.state.description}
                        hintText="Description"
                        multiLine={true}
                        rowsMax={4}
                        fullWidth={true}
                        errorText={this.state.failDescriptionMessage}
                        onChange={this.handleChangeDescription}/>
                    <DatePicker hintText="Portrait Dialog"
                        floatingLabelText="Start date and time"
                        style={dateStyle}
                        mode="landscape"
                        value={new Date(this.state.startAt * 1000)}
                        onChange={this.handleChangeStartAt}/>
                    <TimePicker hintText="12hr Format"
                        style={dateStyle}
                        value={new Date(this.state.startAt * 1000)}
                        format="24hr"
                        onChange={this.handleChangeStartAt}/>
                    <DatePicker hintText="Portrait Dialog"
                        floatingLabelText="Finish date and time"
                        style={dateStyle}
                        mode="landscape"
                        value={new Date(this.state.timeEnd * 1000)}
                        onChange={this.handleChangeTimeEnd}/>
                    <TimePicker hintText="12hr Format"
                        style={dateStyle}
                        value={new Date(this.state.timeEnd * 1000)}
                        format="24hr"
                        onChange={this.handleChangeTimeEnd}/>
                    <SelectField
                        floatingLabelText="Team"
                        value={this.state.team}
                        fullWidth={true}
                        onChange={this.handleChangeTeam}>
                        {
                            this.state.teams.map(team => {
                                return <MenuItem value={team.id} key={team.id} primaryText={team.name} />;
                            })
                        }
                    </SelectField>
                    <TextField
                        hintText="Budget"
                        floatingLabelText="Budget"
                        fullWidth={true}
                        defaultValue={this.state.budget}
                        errorText={this.state.failBudgetMessage}
                        onChange={this.handleChangeBudget}/>
                    <Location
                        formattedAddress={this.state.formattedAddress}
                        changed={this.handleChangeLocation}/>
                    <SelectField
                        floatingLabelText="Status"
                        value={this.state.status}
                        onChange={this.handleChangeStatus}>
                        <MenuItem value={0} primaryText="draft" />
                        <MenuItem value={1} primaryText="published" />
                        <MenuItem value={2} primaryText="going" />
                        <MenuItem value={3} primaryText="finished" />
                    </SelectField>
                    {this.state.openErrorSnackBar &&
                        (<Snackbar
                            open={this.state.openErrorSnackBar}
                            message={this.state.responseError}
                            autoHideDuration={5000}
                            onRequestClose={this.closeErrorSnackBar}
                        />)
                    }
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelCreateDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}

export default CreateEvent;
