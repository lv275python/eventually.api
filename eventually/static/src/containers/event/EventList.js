import React from 'react';
import { getEvents } from './EventService';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import EventLink from './EventLink';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';

const containerStyle = {
    width: '80%',
    margin: '0 auto'
};

const FloatingButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


class EventList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            events: []
        };

    }

    getData = () => {
        getEvents().then(response => {
            this.setState(response.data);
        });
    };

    goToHome = () => {
        this.props.history.push('/home');
    };

    componentWillMount() {
        this.getData();
    }


    render() {
        return (
            <div style={containerStyle}>
                {
                    this.state.events.map(event => (
                        <EventLink
                            key={event.id.toString()}
                            title={event.name}
                            description={event.description}
                            id={event.id}
                        />)
                    )
                }
                <FloatingActionButton
                    onClick={this.goToHome}
                    style={FloatingButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
            </div>
        );
    }
}

export default EventList;
