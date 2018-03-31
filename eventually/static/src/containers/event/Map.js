import React from 'react';
import {compose, withProps} from 'recompose';
import {GoogleMap, Marker, withGoogleMap, withScriptjs} from 'react-google-maps';
import {googleMapsAPIKey} from '../../helper/keys';

const MapComponent = compose(
    withProps({
        googleMapURL:
            `https://maps.googleapis.com/maps/api/js?key=${googleMapsAPIKey}
            &language=en&v=3.exp&libraries=geometry,drawing,places`,
        loadingElement: <div style={{height: '100%'}}/>,
        containerElement: <div style={{height: '200px'}}/>,
        mapElement: <div style={{height: '100%'}}/>
    }),
    withScriptjs,
    withGoogleMap
)(props => (
    <GoogleMap defaultZoom={17} defaultCenter={{lat: props.latitude, lng: props.longitude}} center={{lat: props.latitude, lng: props.longitude}}>
        <Marker position={{lat: props.latitude, lng: props.longitude}} title={props.name}/>
    </GoogleMap>
));

export default MapComponent;
