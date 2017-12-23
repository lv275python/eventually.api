import React from 'react';
import MessageItem from './MessageItem';
import MessagesSender from './MessagesSender';
import Paper from 'material-ui/Paper';

const messagesListWrapperStyles = {
    display: 'flex',
    flexDirection: 'column',

};

const messagesListStyle = {
    overflowY: 'scroll',
    maxHeight: '70vh'
};

export default class MessagesList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            style: this.props.style
        };
    }

    componentWillMount() {
        Object.assign(messagesListWrapperStyles, this.state.style);
        this.setState({
            style: messagesListWrapperStyles
        });
    }

    render() {
        return (
            <div style={this.state.style}>
                <Paper zDepth={2} style={messagesListStyle}>
                    {this.props.messages.map(message => (
                        <MessageItem
                            key={message.id.toString()}
                            author={message.author}
                            avatar={message.avatar}
                            date={message.created_at}
                            text={message.text}
                        />)
                    )}
                </Paper>
                <MessagesSender />
            </div>
        );
    }
}
