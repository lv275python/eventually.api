import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import RaisedButton from 'material-ui/RaisedButton';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';
import { lightGreen400 } from 'material-ui/styles/colors';
import {List, ListItem} from 'material-ui/List';

const styles = {
    raisedButton: {
        marginLeft: 16
    }
};

export default class ParticipantListDialog extends React.Component {
    state = {
        open: false
    };

    handleOpen = () => {
        this.setState({open: true});
    };

    handleClose = () => {
        this.setState({open: false});
    };

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
                    primaryText={this.props.participants[i]}
                />
            );
        }

        return (
            <div>
                <RaisedButton
                    label={this.props.text}
                    onClick={this.handleOpen}
                    style={styles.raisedButton}
                    backgroundColor={lightGreen400}/>
                <Dialog
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
