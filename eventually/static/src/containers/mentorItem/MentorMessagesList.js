import React from 'react';
import MentorMessagesItem from './MentorMessagesItem';
import MentorMessagesSender from './MentorMessagesSender';
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
                            <MentorMessagesItem key={message.id.toString()}
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
