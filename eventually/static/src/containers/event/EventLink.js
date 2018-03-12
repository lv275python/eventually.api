import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import RaisedButton from 'material-ui/RaisedButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import Event from './Event';
import { googleMapsAPIKey } from '../../helper/keys';

const raisedButtonDivStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

const raisedButtonStyle = {
    marginLeft: 10
};

class EventLink extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            address: '',
            teamId: this.props.team
        };
    }

    goToTaskList = () => {
        this.props.history.push('/events/' + this.props.id);
    };

    goToVoting = () => {
        this.props.history.push({
            pathname: '/events/' + this.props.id + '/vote',
            state: {
                teamId: this.state.teamId
            }
        });
    };

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
                let country = this.fetchAddressComponent(addressComponents, 'country');
                let countryName = country ? country.long_name : null;

                let formattedAddress = [countryName, cityName].filter(el => el).join(', ');
                return this.setState({address: formattedAddress});
            }
        });
    }

    fetchAddressComponent(addressComponents, componentType) {
        return addressComponents.find(component => {
            return component.types.indexOf(componentType) !== -1;
        });
    }

    showAddress = () => {
        if (this.state.address) {
            return 'Location: ' + this.state.address;
        } else {
            return '';
        }
    };

    showStartAt = () => {
        if (this.props.start_at) {
            const date = new Date(this.props.start_at * 1000);
            return `Start at: ${date.toDateString()}`;
        } else {
            return '';
        }
    };

    componentWillMount() {
        this.fetchAddress();
    }

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        actAsExpander={true}
                        showExpandableButton={false}
                        title={this.props.name}
                        subtitle={
                            <div>
                                <div>{this.showAddress()}</div>
                                <div>{this.showStartAt()}</div>
                            </div>
                        }
                    />
                    <CardText>
                        {this.props.description}
                    </CardText>

                    <CardActions>
                        <div style={raisedButtonDivStyle}>
                            <RaisedButton
                                style={raisedButtonStyle}
                                label="Details"
                                backgroundColor={lightGreen400}
                                onClick={this.goToTaskList}
                            />
                            <RaisedButton
                                style={raisedButtonStyle}
                                label="Voting"
                                backgroundColor={lightGreen400}
                                onClick={this.goToVoting}
                            />
                        </div>
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(EventLink);
