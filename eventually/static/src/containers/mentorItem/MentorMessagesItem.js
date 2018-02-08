import React from 'react';
import {Card, CardHeader, CardText} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';

const cardHeaderStyle = {
    'display': 'flex',
    'alignItems': 'center',
    'cursor': 'pointer'
};

const titleStyle = {
    'fontWeight': 'bold',
    'fontSize': '16px'
};

const textStyle = {
    'fontSize': '14px'
};

export default class MentorMessagesItem extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div>
                <Card>
                    <CardHeader
                        title={this.props.author}
                        avatar={<Avatar src={'https://robohash.org/' + this.props.avatar}/>}
                        style={cardHeaderStyle}
                        titleStyle={titleStyle}
                    />
                    <CardText style={textStyle}>
                        {this.props.text}
                    </CardText>
                </Card>
            </div>
        );
    }
}
