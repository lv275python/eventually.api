import React from 'react';
import { putEventService, getEvent } from './EventService';
import DatePicker from 'material-ui/DatePicker';
import TimePicker from 'material-ui/TimePicker';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import {CancelDialog} from 'src/containers';
import Location from './GoogleLocation';
import {googleMapsAPIKey} from 'src/helper/keys';
import isEqual from 'lodash/isEqual';


const dateStyle = {
    display: 'inline-block',
    width: '50%'
};

export default class EventEdit extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.id,
            open: false,
            owner: this.props.owner,
            name: this.props.name,
            description: this.props.description,
            startAt: this.props.startAt,
            duration: this.props.duration,
            budget: this.props.budget ? this.props.budget : 0,
            status: this.props.status,
            openCancelDialog: false,
            formattedAddress: 'lon',
            longitude: this.props.longitude,
            latitude: this.props.latitude
        };
    }

    componentWillMount(){
        this.fetchAddress();
    }

    fetchAddress() {
        const googleMapsClient = require('@google/maps').createClient({
            key: googleMapsAPIKey
        });
        let location = [this.props.latitude, this.props.longitude];
        googleMapsClient.reverseGeocode({'latlng': location}, (err, response) => {
            if (response.status == 200) {
                let addressComponents = response.json.results[0].address_components;
                let city = this.fetchAddressComponent(addressComponents, 'locality');
                let cityName = city ? city.short_name : null;
                let street = this.fetchAddressComponent(addressComponents, 'route');
                let streetName = street ? street.long_name : null;
                let number = this.fetchAddressComponent(addressComponents, 'street_number');
                let numberStreet = number ? number.long_name : null;
                let formattedAddress = [streetName, cityName,numberStreet].filter(el => el).join(', ');
                return this.setState({formattedAddress: formattedAddress});
            }
        });
    }

    fetchAddressComponent(addressComponents, componentType) {
        return addressComponents.find(component => {
            return component.types.indexOf(componentType) !== -1;
        });
    }

    handleOpen = () => {
        this.setState({ open: true });
    };

    handleClose = () => {
        this.setState ({
            open: false,
            name: this.props.name,
            description: this.props.description,
            startAt: this.props.startAt,
            duration: this.props.duration,
            budget: this.props.budget ? this.props.budget : 0,
            status: this.props.status,
            longitude: this.props.longitude,
            latitude: this.props.latitude
        });
    };

    handleSave = () => {
        const name = this.state.name;
        const description = this.state.description;
        const startAt = this.state.startAt;
        const budget = this.state.budget;
        const status = this.state.status;
        const duration = this.state.duration;
        const latitude = this.state.latitude;
        const longitude = this.state.longitude;
        putEventService( this.state.eventId, name, description, startAt, budget, status, duration, latitude, longitude).then(response => {
            getEvent(this.state.eventId).then(response =>{
                this.props.editEvent(response.data);
            });
        });
        this.setState ({ open: false});
    };


    handleName = event => {
        this.setState({name: event.target.value});
    };

    handleDescription = event => {
        this.setState({description: event.target.value});
    };

    handleStartAt = (event, date) => {
        this.setState({startAt: date/1000});
    };

    handleDuration = (event, date) => {
        const duration = (date/1000)-this.state.startAt;
        this.setState({duration: duration });
    };

    handleBudget = event => {
        this.setState({budget: +event.target.value});
    };

    handleStatus = (event, index, status) => {
        this.setState({status});
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelEditDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if (
            (this.state.name != this.props.name) ||
            (this.state.description != this.props.description) ||
            (this.state.startAt != this.props.startAt) ||
            (this.state.budget != this.props.budget) ||
            (this.state.status != this.props.status) ||
            (this.state.duration != this.props.duration)||
            (this.state.longitude != this.props.longitude)||
            (this.state.latitude != this.props.latitude)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleClose();
    };

    handleChangeLocation = value => {
        this.setState({
            formattedAddress: value.formattedAddress,
            longitude: value.location.lng,
            latitude: value.location.lat,
        });
    };

    render() {
        const actions = [
            <FlatButton
                id = "cancel-button"
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                id = "save-button"
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
                        id = "edit-button"
                        label="Edit"
                        primary={true}
                        keyboardFocused={true}
                        onClick={this.handleOpen}
                    />
                    <Dialog
                        id = "dialog-buttons"
                        title={this.props.title}
                        actions={actions}
                        modal={false}
                        open={this.state.open}
                        onRequestClose={this.handleRequestClose}
                        autoScrollBodyContent={true}
                        style={{zIndex: 800}}
                    >
                        <TextField
                            id = "name-input"
                            floatingLabelText="Name:"
                            onChange={this.handleName}
                            hintText='Name'
                            value={this.state.name}
                            fullWidth={true}
                        />
                        <TextField
                            id = "description-input"
                            floatingLabelText="Description:"
                            onChange={this.handleDescription}
                            hintText='Description'
                            value={this.state.description}
                            fullWidth={true}
                        />
                        <DatePicker
                            id ="start-date-input"
                            floatingLabelText="Start date and time."
                            onChange={this.handleStartAt}
                            mode="landscape"
                            style={dateStyle}
                            fullWidth={true}
                            value={new Date(this.state.startAt*1000)}
                        />
                        <TimePicker
                            textFieldStyle={{width: '100%'}}
                            format="24hr"
                            hintText="24hr Format"
                            style={dateStyle}
                            value={new Date(this.state.startAt*1000)}
                            onChange={this.handleStartAt}
                        />
                        <DatePicker
                            id = "end-date-input"
                            floatingLabelText="End date and time."
                            onChange={this.handleDuration}
                            mode="landscape"
                            style={dateStyle}
                            fullWidth={true}
                            value={new Date((this.state.startAt+this.state.duration)*1000)}
                        />
                        <TimePicker
                            textFieldStyle={{width: '100%'}}
                            format="24hr"
                            hintText="24hr Format"
                            style={dateStyle}
                            value={new Date((this.state.startAt+this.state.duration)*1000)}
                            onChange={this.handleDuration}
                        />
                        <TextField
                            id = "budget-input"
                            floatingLabelText="Budget:"
                            onChange={this.handleBudget}
                            hintText='Budget'
                            value={this.state.budget}
                            fullWidth={true}
                        />
                        <Location
                            formattedAddress={this.state.formattedAddress}
                            changed={this.handleChangeLocation}
                        />
                        <SelectField
                            id = "status-input"
                            floatingLabelText="Status"
                            onChange={this.handleStatus}
                            value={this.state.status}
                        >
                            <MenuItem value={0} primaryText="Draft" />
                            <MenuItem value={1} primaryText="Published" />
                            <MenuItem value={2} primaryText="Going" />
                            <MenuItem value={3} primaryText="Finished" />
                        </SelectField>
                    </Dialog>
                </form>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelEditDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}
