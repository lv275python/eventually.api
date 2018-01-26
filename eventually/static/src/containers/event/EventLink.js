import React from 'react';
import { Card, CardActions, CardHeader, CardText } from 'material-ui/Card';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';

const raiseButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end'
};

class EventLink extends React.Component {

    constructor(props) {
        super(props);
    }

    goToHome = () => {
        this.props.history.push('/events/' + 1);
    };

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        actAsExpander={true}
                        showExpandableButton={false}
                        title={this.props.title}
                        subtitle={this.props.description}
                    />
                    <CardActions>
                        <div style={raiseButtonStyle}>
                            <RaisedButton
                                label="Details"
                                backgroundColor={lightGreen400}
                                onClick={this.goToHome} />
                        </div>
                    </CardActions>
                </Card>
            </div >
        );
    }
}
export default withRouter(EventLink);
