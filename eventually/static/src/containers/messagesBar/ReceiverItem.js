import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import ChatBubble from 'material-ui/svg-icons/communication/chat-bubble';
import {lightGreen200, lightGreen500, yellow200, grey300} from 'material-ui/styles/colors';

const avatarStyle = {
    margin: 10
};

const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    width: '90%'
};

const invisibleCardHeaderStyle = {
    display: 'none'
};

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '14px',
};

const activityChatBubbleStyle = {
    true: {
        color: lightGreen500,
        marginRight: '5%',
        width: '10%'
    },
    false: {
        color: grey300,
        marginRight: '5%',
        width: '10%'
    }
};

export default class ReceiverItem extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isVisible: this.props.isVisible,
            isActive: this.props.isActive,
            isHovered: false
        };
    }

    componentWillReceiveProps(nextProps){
        this.setState({isVisible: nextProps.isVisible});
    }

    handleClick = () => {
        this.props.onReceiverClick(this.props.id);
    };

    handleMouseEnter = () => {
        this.setState({
            isHovered: true
        });
    };

    handleMouseLeave = () => {
        this.setState({
            isHovered: false
        });
    };

    render() {

        let chatBubble = null,
            contentWrapperStyle = {
                display: 'flex',
                alignItems: 'center'
            };

        if (this.state.isVisible) {
            chatBubble = (<ChatBubble style={activityChatBubbleStyle[this.props.isOnline]} />);
            contentWrapperStyle.justifyContent = 'space-between';

            if (this.props.isActive) {
                contentWrapperStyle.backgroundColor = lightGreen200;
            }

            if (this.state.isHovered) {
                contentWrapperStyle.backgroundColor = yellow200;
            }

        } else {
            contentWrapperStyle.justifyContent = 'center';

            if (this.props.isActive) {
                contentWrapperStyle.backgroundColor = lightGreen200;
            }
        }

        return (
            <div>
                <Card>
                    <div
                        style={contentWrapperStyle}
                        onMouseEnter={this.handleMouseEnter}
                        onMouseLeave={this.handleMouseLeave}>
                        <Avatar src={`https://robohash.org/${this.props.avatar}`} style={avatarStyle} />
                        <CardHeader
                            style={this.state.isVisible ? cardHeaderStyle : invisibleCardHeaderStyle}
                            title={`${this.props.firstName} ${this.props.lastName}`}
                            titleStyle={titleStyle}
                            onClick={this.handleClick}
                        />
                        {chatBubble}
                    </div>
                </Card>
            </div>
        );
    }
}
