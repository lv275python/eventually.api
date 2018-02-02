import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';
import Event from '../eventItem/Event';


const raiseButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

class EventLink extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            address: ''
        };
    }

    goToTaskList = () => {
        this.props.history.push({
            pathname: '/events/' + this.props.id + '/task',
            state: {
                event: {
                    team: this.props.team,
                    owner: this.props.owner,
                    name: this.props.name,
                    description: this.props.description,
                    start_at: this.props.start_at,
                    created_at: this.props.created_at,
                    updated_at: this.props.updated_at,
                    duration: this.props.duration,
                    longitude: this.props.longitude,
                    latitude: this.props.latitude,
                    budget: this.props.budget,
                    status: this.props.status
                }
            }
        });
    };

    fetchAddress() {
        const googleMapsClient = require('@google/maps').createClient({
            key: 'AIzaSyDDuGt0E5IEGkcE6ZfrKfUtE9Ko_de66pA'
        });
        let location = [this.props.latitude, this.props.longitude];

        googleMapsClient.reverseGeocode({'latlng': location}, (err, response) => {
            if (response.status == 200) {
                let addressComponents = response.json.results[0].address_components;
                let city = this.fetchAddressComponent(addressComponents, 'locality');
                let city_name = city ? city.short_name : null;
                let country = this.fetchAddressComponent(addressComponents, 'country');
                let country_name = country ? country.long_name : null;

                let formattedAddress = [country_name, city_name].filter(el => el).join(', ');
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
                        subtitle={this.showAddress()}
                    />
                    <CardText>
                        {this.props.description}
                    </CardText>

                    <CardActions>
                        <RaisedButton label="Tasks" onClick={this.goToTaskList} />
                        <Event
                            key={this.props.id.toString()}
                            team={this.props.team}
                            owner={this.props.owner}
                            name={this.props.name}
                            description={this.props.description}
                            start_at={this.props.start_at}
                            created_at={this.props.created_at}
                            updated_at={this.props.updated_at}
                            duration={this.props.duration}
                            longitude={this.props.longitude}
                            latitude={this.props.latitude}
                            budget={this.props.budget}
                            status={this.props.status}
                            id={this.props.id}
                        />
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(EventLink);
