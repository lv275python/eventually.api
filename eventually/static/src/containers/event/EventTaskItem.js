import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import {Card, CardHeader, CardText} from 'material-ui/Card';

export default class EventTaskItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            title: this.props.title,
            description: this.props.description.slice(0,300)+'...',
            status: this.props.status
        };
    }

    render() {
        return (
            <Card>
                <CardHeader
                    title={this.state.title}
                    actAsExpander={true}
                    showExpandableButton={true}
                />
                <CardText expandable={true}>
                    {this.state.description}
                </CardText>
            </Card>
        );
    }
}

