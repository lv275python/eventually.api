import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import IconLocationOn from 'material-ui/svg-icons/communication/location-on';
import RaisedButton from 'material-ui/RaisedButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import Event from './Event';
import { googleMapsAPIKey } from '../../helper/keys';
import ActionSchedule from 'material-ui/svg-icons/action/schedule';


const styles = {
    raisedButtonDiv: {
        display: 'flex',
        justifyContent: 'flex-end'
    },
    raisedButton: {
        marginLeft: 10,
        borderRadius: '10px'
    },
    iconLocationOn: {
        float: 'left',
        color: '#777777'
    },
    address: {
        lineHeight: '24px',
        verticalAlign: 'middle'
    },
    actionScheduleContainer: {
        clear: 'both',
        marginTop: '3px'
    },
    actionSchedule: {
        verticalAlign: 'middle',
        color: '#12bbd2'
    },
    card: {
        borderRadius: '0 20px',
        marginTop: '10px',
        border: '1px solid #12bbd2'
    },
    cardHeader: {
        display: 'block',
        fontWeight: 'bold',
        padding: '5px'
    },
    cardHeaderTitle: {
        textAlign: 'center',
        fontSize: '20px'
    }
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
                teamId: this.state.teamId,
                startAt: this.props.start_at
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
            return (
                <div>
                    <IconLocationOn
                        style={styles.iconLocationOn}
                    />
                    <div style={styles.address}>
                        {this.state.address}
                    </div>
                </div>
            );
        } else {
            return '';
        }
    };

    showStartAt = () => {
        if (this.props.start_at) {
            const date = new Date(this.props.start_at * 1000);
            return (
                <div style={styles.actionScheduleContainer}>
                    <ActionSchedule
                        style={styles.actionSchedule}
                    />
                    {`${date.toDateString()}`}
                </div>
            );
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
                <Card
                    style={styles.card}
                    zDepth={3}
                >
                    <CardHeader
                        style={styles.cardHeader}
                        textStyle={styles.cardHeader}
                        actAsExpander={true}
                        showExpandableButton={false}
                        title={this.props.name}
                        titleStyle={styles.cardHeaderTitle}
                        subtitleStyle={{width: '100%'}}
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
                        <div style={styles.raisedButtonDiv}>
                            <RaisedButton
                                style={styles.raisedButton}
                                label="Details"
                                backgroundColor={lightGreen400}
                                onClick={this.goToTaskList}
                            />
                            <RaisedButton
                                style={styles.raisedButton}
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
