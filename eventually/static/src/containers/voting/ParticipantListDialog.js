import React from 'react';
import Avatar from 'material-ui/Avatar';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import {List, ListItem} from 'material-ui/List';
import {getImageUrl} from 'src/helper';

export default class ParticipantListDialog extends React.Component {
    state = {
        open: this.props.open
    };

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
        this.props.handleCloseParticipants();
    };

    componentWillReceiveProps(nextProps) {
        this.setState({
            open: nextProps.open
        });
    }

    render() {
        const actions = [
            <FlatButton
                label="Ok"
                primary={true}
                keyboardFocused={true}
                onClick={this.handleClose}
            />
        ];
        const participantsCount = this.props.participants.length;
        const items = [];
        for (let i = 0; i < participantsCount; i++) {
            items.push(
                <ListItem
                    key={i}
                    primaryText={this.props.participants[i].name}
                    leftAvatar={<Avatar src={getImageUrl(this.props.participants[i].photo)} />}
                />
            );
        }

        return (
            <div>
                <Dialog
                    contentStyle={{width: '40%', minWidth: 300}} 
                    title={this.props.text}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    autoScrollBodyContent={true}>
                    <List>
                        {items}
                    </List>
                </Dialog>
            </div>
        );
    }
}
