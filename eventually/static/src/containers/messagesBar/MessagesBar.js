import React from 'react';
import MessagesList from './MessagesList';
import ReceiversList from './ReceiversList';
import { getReceiversList, getMessagesList, postChatMessage, getOnlineUsers } from './messagesBarService';

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
            nextPage: 1,
            requestIntervalId: null,
            receivers: []
        };
    }

    componentWillMount() {
        const receiversObject = this.props.location === 'progress' ? getReceiversList() : getReceiversList(true);
        const requestIntervalId = setInterval(this.handleOnlineStatus, 5000);
        this.setState({
            receivers: receiversObject.receivers,
            requestIntervalId: requestIntervalId
        });
    }

    componentWillUnmount() {
        clearInterval(this.state.requestIntervalId);
    }

    handleOnlineStatus = () => {
        const users = this.state.receivers.map(receiver => {
            return receiver.id;
        });
        getOnlineUsers(users)
            .then(response => {
                const data = response.data;
                const updatedRecivers = this.state.receivers.map(receiver => {
                    receiver.is_online = !!data[receiver.id];
                    return receiver;
                });
                this.setState({
                    receivers: updatedRecivers
                });
            });
    }

    handleReceiverClick = receiverId => {
        const nextPage = receiverId === this.state.activeReceiverItem ? this.state.nextPage : 1;
        getMessagesList(receiverId, nextPage)
            .then(response => {
                const data = response.data;
                this.setState({
                    isMessagesList: true,
                    isReceiversList: false,
                    activeReceiverItem: receiverId,
                    nextPage: data.next_page,
                    messages: data.messages
                });
            })
            .catch(error => {
                console.log(error);
            });
    };

    getMessages = (receiverId, pageNumber) => {
        getMessagesList(receiverId, pageNumber)
            .then(response => {
                let messages = response.data.messages ? this.state.messages.concat(response.data.messages) : this.state.messages;
                this.setState({ 'messages': messages });
                return true;
            })
            .catch(error => {
                console.log(error);
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
    }

    handleShowMoreClick = () => {
        getMessagesList(this.state.activeReceiverItem, this.state.nextPage)
            .then(response => {
                const data = response.data,
                    messages = data.messages ? this.state.messages.concat(data.messages) : this.state.messages;

                this.setState({
                    messages: messages,
                    nextPage: data.next_page
                });
            })
            .catch(error => {
                console.log(error);
            });
    }

    render() {
        const isShowMoreButton = this.state.nextPage !== -1;
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
