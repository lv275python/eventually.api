import React from 'react';
import { getEvents } from './EventService';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import EventLink from './EventLink';
import ContentAdd from 'material-ui/svg-icons/content/add';
import CreateEvent from './CreateEvent';
import injectTapEventPlugin from 'react-tap-event-plugin';
import Pagination from 'material-ui-pagination';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';

injectTapEventPlugin();

const styles = {
    fullContainer: {
        width: '90%',
        margin: '0 auto'
    },
    container: {
        width: '75%',
        float: 'left'
    },
    pagination: {
        margin: '0 auto',
        textAlign: 'center'
    },
    customWidth: {
        width: 180,
        marginLeft: '3%'
    }
};

class EventList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            events: [],
            fullLength: 0,
            total: 0,
            display: 5,
            number: 1,
            value: 2,
            limit: 2
        };
    }

    getData = (limit, number) => {
        getEvents(limit, number).then(response => {
            this.setState({
                events: response.data.events,
                fullLength: response.data.full_length,
                total: this.getPagesAmount(response.data.full_length),
                limit: limit
            });
        });
    };

    getPagesAmount = (fullLength) => {
        const limit = this.state.limit;
        if (fullLength % limit == 0) {
            return fullLength / limit;
        } else {
            return Math.ceil(fullLength / limit);
        }
    };

    componentWillMount() {
        this.getData(this.state.limit, 1);
    }

    getEventLinks() {
        return this.state.events.map(event => {
            return <EventLink
                key={event.id.toString()}
                team={event.team}
                owner={event.owner}
                name={event.name}
                description={event.description}
                start_at={event.start_at}
                created_at={event.created_at}
                updated_at={event.updated_at}
                duration={event.duration}
                longitude={event.longitude}
                latitude={event.latitude}
                budget={event.budget}
                status={event.status}
                id={event.id}
            />;
        });
    }

    handleChangeSelectField = (event, index, value) => {
        const number = 1;
        this.getData(value, number);
        this.setState({
            value: value,
            limit: value,
            number: number
        });
    };

    handleChangePagination = number => {
        this.getData(this.state.limit, number);
        this.setState({ number });
    };

    getPagination() {
        if (this.state.fullLength > this.state.limit) {
            return <Pagination
                total = { this.state.total }
                current = { this.state.number }
                display = { this.state.display }
                onChange = { this.handleChangePagination }
            />;
        }
    }

    addEvent = (newEvent) => {
        this.state.events.unshift(newEvent);
        this.setState({
            events: this.state.events
        });
    };

    render() {
        return (
            <div style={styles.fullContainer}>
                <div style={styles.container}>
                    {this.getEventLinks()}
                    <CreateEvent
                        addEvent={this.addEvent}
                    />
                    <div style={styles.pagination}>
                        {this.getPagination()}
                    </div>
                </div>
                <SelectField
                    floatingLabelText="Events per page:"
                    value={this.state.value}
                    onChange={this.handleChangeSelectField}
                    style={styles.customWidth}
                >
                    <MenuItem value={2} primaryText="2" />
                    <MenuItem value={5} primaryText="5" />
                    <MenuItem value={10} primaryText="10" />
                </SelectField>
            </div>
        );
    }
}

export default EventList;
