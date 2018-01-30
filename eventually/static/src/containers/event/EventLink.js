import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';
// import {createClient} from '@google/maps';

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

    // console.log(parseInt(this.props.match.params.eventId, 10)); //==> id
    // console.log(this.props.location.state.event); // ==> event data

    goToEvent = () => {
        this.props.history.push({
            pathname: '/events/' + this.props.id,
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

    // fetchAddress() {
    //   const googleMaps = createClient({
    //       key: 'AIzaSyDDuGt0E5IEGkcE6ZfrKfUtE9Ko_de66pA'
    //   });
    //   // var geocoder = googleMaps.Geocoder();
    //   // var location = googleMaps.LatLng(this.props.latitude, this.props.longitude);
    //
    //   googleMaps.geocode({'bounds': [this.props.latitude, this.props.longitude]}, (results, status) => {
    //       if (status == google.maps.GeocoderStatus.OK) {
    //         var addressComponents = results[0].address_components;
    //         // console.log(addressComponents);
    //         var city = this.fetchAddressComponent(addressComponents, 'locality');
    //         var city_name = city ? city.short_name : null;
    //         var country = this.fetchAddressComponent(addressComponents, 'country');
    //         var country_name = country ? country.long_name : null;
    //
    //         var formattedAddress = [country_name, city_name].filter(el => el).join(', ');
    //         return this.setState({address: formattedAddress});
    //       }
    //     }
    //   );
    // }

    fetchAddressComponent(addressComponents, componentType) {
        return addressComponents.find(component => {
            return component.types.indexOf(componentType) !== -1;
        });
    }

    // componentWillMount() {
    //     this.fetchAddress();
    // }

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        actAsExpander={true}
                        showExpandableButton={false}
                        title={this.props.name}
                        subtitle={this.props.longitude + ', ' + this.props.latitude}
                    />
                    <CardActions>
                        <div style={raiseButtonStyle}>
                            <RaisedButton
                                label="Details"
                                backgroundColor={lightGreen400}
                                onClick={this.goToEvent}>
                            </RaisedButton>
                        </div>
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(EventLink);
