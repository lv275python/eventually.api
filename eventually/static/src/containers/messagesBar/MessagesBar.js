import React from 'react';
import MessagesList from './MessagesList';
import ReceiversList from './ReceiversList';
import { getReceiversList, getMessagesList, postChatMessage, getOnlineUsers } from './messagesBarService';
import { getMessagesSet, getNextPageNumber } from './messagesBarHelper';

const messagesListStyle = {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'space-between',
    position: 'absolute',
    top: 0,
    width: '80%',
    marginRight: '20%',
    height: '90vh'
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
            receivers: [],
            activeReceiverItem: -1,
            messages: [],
            defaultPage: 1,
            nextPage: null,
            requestIntervalId: null,
            messagesRefreshId: null
        };
    }

    componentWillMount() {
        const receiversObject = this.props.location === 'progress' ? getReceiversList() : getReceiversList(true);
        const requestIntervalId = setInterval(this.handleOnlineStatus, 5000);
        const messagesRefreshId = setInterval(this.handleMessagesRefresh, 5000);
        this.setState({
            receivers: receiversObject.receivers,
            requestIntervalId: requestIntervalId,
            messagesRefreshId: messagesRefreshId
        });
    }

    componentWillUnmount() {
        clearInterval(this.state.requestIntervalId);
        clearInterval(this.state.messagesRefreshId);
    }

    handleOnlineStatus = () => {
        const users = this.state.receivers.map(receiver => {
            return receiver.id;
        });
        getOnlineUsers(users)
            .then(response => {
                const data = response.data;
                const updatedReceivers = this.state.receivers.map(receiver => {
                    receiver.is_online = !!data[receiver.id];
                    return receiver;
                });
                this.setState({
                    receivers: updatedReceivers
                });
            });
    };

    handleMessagesRefresh = () => {
        getMessagesList(this.state.activeReceiverItem, this.state.defaultPage)
            .then(response => {
                const data = response.data;
                if (data.messages) {
                    const allMessages = this.state.messages.concat(data.messages),
                        messages = getMessagesSet(allMessages),
                        actualNextPage = getNextPageNumber(messages, this.state.defaultPage, data.per_page);
                    this.setState({
                        messages: messages,
                        nextPage: this.state.nextPage === -1 ? this.state.nextPage : actualNextPage
                    });
                }
            });
    };

    handleReceiverClick = receiverId => {
        getMessagesList(receiverId, this.state.defaultPage)
            .then(response => {
                const data = response.data;
                this.setState({
                    isMessagesList: true,
                    isReceiversList: false,
                    activeReceiverItem: receiverId,
                    nextPage: data.next_page,
                    messages: data.messages
                });
            });
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
    };

    handleShowMoreClick = () => {
        getMessagesList(this.state.activeReceiverItem, this.state.nextPage)
            .then(response => {
                const data = response.data,
                    allMessages = this.state.messages.concat(data.messages),
                    messages = getMessagesSet(allMessages);

                this.setState({
                    messages: messages,
                    nextPage: data.next_page
                });
            });
    };

    render() {
        const isShowMoreButton = this.state.nextPage > 1;
        const messagesList = this.state.isMessagesList ?
            <MessagesList
                style={messagesListStyle}
                messages={this.state.messages}
                receiverId={this.state.activeReceiverItem}
                onSendClick={this.handleSendClick}
                onShowMoreClick={this.handleShowMoreClick}
                isShowMoreButton={isShowMoreButton}
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
