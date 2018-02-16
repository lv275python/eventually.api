import React, {Component} from 'react';
import TextField from 'material-ui/TextField';
import { googleMapsAPIKey } from '../../helper/keys';
import { compose, withProps, lifecycle } from 'recompose';
import { withScriptjs } from 'react-google-maps';
import { StandaloneSearchBox } from 'react-google-maps/lib/components/places/StandaloneSearchBox';


const textFieldStyle = {
    field: {
        fontSize: 14
    }
};

class Location extends Component {
    shouldComponentUpdate(nextProps, nextState){
        return false;
    }

    render() {
        const PlacesWithStandaloneSearchBox = compose(
            withProps({
                changed: this.props.changed,
                googleMapURL: 'https://maps.googleapis.com/maps/api/js?key=' + googleMapsAPIKey + '&libraries=geometry,drawing,places',
                loadingElement: <div style={{ height: '100%' }} />,
                containerElement: <div style={{ height: '400px'}} />,
            }),
            lifecycle({
                componentWillMount() {
                    const refs = {};

                    this.setState({
                        places: [],
                        onSearchBoxMounted: ref => {
                            refs.searchBox = ref;
                        },
                        onPlacesChanged: () => {
                            const places = refs.searchBox.getPlaces();
                            const data = {
                                location: {
                                    lat: places[0].geometry.location.lat(),
                                    lng: places[0].geometry.location.lng()
                                },
                                formattedAddress: places[0].formatted_address
                            };
                            this.props.changed(data);
                        },
                    });
                },
            }),
            withScriptjs)(props =>
            <div>
                <StandaloneSearchBox
                    ref={props.onSearchBoxMounted}
                    onPlacesChanged={props.onPlacesChanged}
                >
                    <TextField
                        name='location'
                        placeholder="Enter address"
                        defaultValue={this.props.formattedAddress}
                        fullWidth={true}
                        inputStyle={textFieldStyle.field}
                    />
                </StandaloneSearchBox>
            </div>
        );
        return <PlacesWithStandaloneSearchBox />;
    }
}

export default Location;
