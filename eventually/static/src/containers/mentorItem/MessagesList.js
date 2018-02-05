import React from 'react';
import MentorMessageItem from './MessageItem';
import MentorMessagesSender from './MessagesSender';
import Paper from 'material-ui/Paper';

export default class MentorMessagesList extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={this.props.style}>
                <MessagesSender />
                <Paper zDepth={2}>
                    {
                        this.props.messages.map(message => (
                            <MessageItem key={message.id.toString()}
                                author={message.author}
                                avatar={message.avatar}
                                text={message.text}
                            />
                        )
                        )
                    }
                </Paper>
            </div>
        );
    }
}
