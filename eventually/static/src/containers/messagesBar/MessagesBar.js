import React from 'react';
import MessagesList from './MessagesList';
import ReceiversList from './ReceiversList';
import { getReceiversList, getMessagesList, postChatMessage } from './messagesBarService';

const messagesListStyle = {
    display: 'flex',
    flexDirection: 'column',
    position: 'absolute',
    top: 0,
    width: '80%',
    marginRight: '20%'
};

export default class MessagesBar extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            style: this.props.style,
            isMessagesList: false,
            isReceiversList: true,
            receiversListExpandedWidth: this.props.expandedWidth,
            receiversListWrappedWidth: this.props.wrappedWidth,
            activeReceiverItem: -1,
            messages: [],
            pageNumber: 1
        };

    }
    componentWillMount() {
        const receiversObject = this.props.location === 'progress' ? getReceiversList() : getReceiversList(true);
        this.setState({
            receivers: receiversObject.receivers
        });
    }

    shouldComponentUpdate(nextProps, nextState) {
        if (nextState.messages) {
            return true;
        }
        return false;
    }

    handleReceiverClick = receiverId => {
        this.setState({
            isMessagesList: true,
            isReceiversList: false,
            activeReceiverItem: receiverId,
            messages: [],
            pageNumber: 1
        });
        this.getMessages(receiverId, this.state.pageNumber);
    };

    getMessages = (receiverId, pageNumber) => {

        getMessagesList(receiverId, pageNumber)
            .then(response => {
                let messages = response.data.messages ? this.state.messages.concat(response.data.messages) : this.state.messages;
                this.setState({ 'messages': messages });
            })
            .catch((error) => {});
    };

    handleReceiversListMouseOver = () => {
        this.setState({
            isReceiversList: true
        });
    };

    handleReceiversListMouseLeave = () => {
        this.setState({
            isReceiversList: false
        });
    };

    handleSendClick = (receiverId, text) => {
        postChatMessage(receiverId, text);
    }

    handleShowMoreClick = () => {
        this.setState({
            pageNumber: ++this.state.pageNumber
        });
        this.getMessages(this.state.activeReceiverItem, this.state.pageNumber);
    }


    render() {
        let messagesList = this.state.isMessagesList ?
            <MessagesList
                style={messagesListStyle}
                messages={this.state.messages}
                receiverId={this.state.activeReceiverItem}
                onSendClick={this.handleSendClick}
                onShowMoreClick={this.handleShowMoreClick}
            /> :
            null;

        return (
            <div style={this.state.style}>
                <ReceiversList
                    receivers={this.state.receivers}
                    isExpanded={this.state.isReceiversList}
                    expandedWidth={this.state.receiversListExpandedWidth}
                    wrappedWidth={this.state.receiversListWrappedWidth}
                    onReceiverClick={this.handleReceiverClick}
                    onMouseOver={this.handleReceiversListMouseOver}
                    onMouseLeave={this.handleReceiversListMouseLeave}
                    activeReceiverItem={this.state.activeReceiverItem}
                />
                {messagesList}
            </div>
        );
    }
}
