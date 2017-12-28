import React from 'react';
import ReceiverItem from './ReceiverItem';
import Drawer from 'material-ui/Drawer';

const receiversListStyle = {
    overflow: 'hidden'
};

const drawerStyle = {
    position: 'relative',
    maxWidth: '100%',
    zIndex: 1100
};

const receiversListWrapperStyle = {
    display: 'flex',
    justifyContent: 'flex-end',
    height: '90vh'
};

export default class ReceiversList extends React.Component {

    constructor(props) {
        super(props);
    }

    handleReceiverClick = this.props.onReceiverClick;
    handleMouseOver = this.props.onMouseOver;
    handleMouseLeave = this.props.onMouseLeave;

    render() {
        return(
            <div
                onMouseEnter={this.handleMouseOver}
                onMouseLeave={this.handleMouseLeave}
                style={receiversListWrapperStyle}
            >
                <Drawer
                    open={true}
                    openSecondary={true}
                    width={this.props.isExpanded ? this.props.expandedWidth : this.props.wrappedWidth}
                    containerStyle={drawerStyle}
                >
                    <div style={receiversListStyle}>
                        {this.props.receivers.map(receiver => (
                            <ReceiverItem
                                key={receiver.id.toString()}
                                id={receiver.id}
                                firstName={receiver.first_name}
                                lastName={receiver.last_name}
                                avatar={receiver.avatar}
                                isOnline={receiver.is_online}
                                onReceiverClick={this.handleReceiverClick}
                                isVisible={this.props.isExpanded}
                                isActive={receiver.id === this.props.activeReceiverItem || false }
                            />
                        ))}
                    </div>
                </Drawer>
            </div>
        );
    }
}
