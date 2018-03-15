import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import injectTapEventPlugin from 'react-tap-event-plugin';
import Badge from 'material-ui/Badge';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import DatePicker from 'material-ui/DatePicker';
import MenuItem from 'material-ui/MenuItem';
import Pagination from 'material-ui-pagination';
import SelectField from 'material-ui/SelectField';
import CreateEvent from './CreateEvent';
import EventLink from './EventLink';
import { getEvents } from './EventService';

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
            limit: 2,
            minDateInSeconds: new Date() / 1000
        };
    }

    getData = (limit, number, minDateInSeconds) => {
        getEvents(limit, number, minDateInSeconds).then(response => {
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
        this.getData(this.state.limit, 1, this.state.minDateInSeconds);
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
        this.getData(value, number, this.state.minDateInSeconds);
        this.setState({
            limit: value,
            number: number
        });
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
        this.state.events.pop();
        this.setState({
            events: this.state.events,
            fullLength: this.state.fullLength + 1,
            total: this.getPagesAmount(this.state.fullLength + 1)
        });
    };

    handleChangePagination = number => {
        this.getData(this.state.limit, number, this.state.minDateInSeconds);
        this.setState({ number });
    };

    handleChangeMinDate = (event, date) => {
        this.getData(this.state.limit, this.state.number, date / 1000);
        this.setState({
            minDateInSeconds: date / 1000
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
                <div>
                    <SelectField
                        floatingLabelText="Events per page:"
                        value={this.state.limit}
                        onChange={this.handleChangeSelectField}
                        style={styles.customWidth}
                    >
                        <MenuItem value={2} primaryText="2" />
                        <MenuItem value={5} primaryText="5" />
                        <MenuItem value={10} primaryText="10" />
                    </SelectField>
                    <DatePicker
                        onChange={this.handleChangeMinDate}
                        floatingLabelText="Min Date"
                        defaultDate={new Date(this.state.minDateInSeconds * 1000)}
                        textFieldStyle={styles.customWidth}
                    />
                </div>
            </div>
        );
    }
}

export default EventList;
