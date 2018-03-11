import React from 'react';
import RaisedButton from 'material-ui/RaisedButton';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import { redA700 } from 'material-ui/styles/colors';
import { eventServiceDelete } from './EventService';
import { getUserId } from 'src/helper';
import { withRouter } from 'react-router-dom';


const styleButton = {
    margin: '5% 5%',
    float: 'left',
};

class DeleteEventDialog extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            eventId: this.props.id,
            open: false,
            name: this.props.name,
            owner: this.props.owner,
        };
    }
    /*Handles open DeleteEventDialog*/
    handleOpen = () => {
        this.setState({ open: true });
    };
    /*Handles close DeleteEventDialog*/
    handleClose = () => {
        this.setState({ open: false });
    };

    deleteEvent = () => {
        eventServiceDelete(this.state.eventId).then(response => {
            if (response.status == 200) {
                this.handleClose();
                this.props.history.push('/events');
            }
        });
    }

    /*checks if user is creator of event*/
    ownerCheck = () => {
        if (getUserId() == this.state.owner){
            return true;
        } else {
            return false;
        }
    }

    render() {
        const actions = [
            <RaisedButton
                backgroundColor={redA700}
                labelColor="#FFF"
                label="Yes"
                onClick={this.deleteEvent}
            />,
            <FlatButton
                label="No"
                primary={true}
                onClick={this.handleClose}
            />
        ];

        let delButton;
        if (this.ownerCheck()==true) {
            delButton = <RaisedButton
                label="Delete"
                backgroundColor="#D50000"
                labelColor="#FFF"
                style={styleButton}
                onClick={this.handleOpen}
            />;
        } else {
            delButton = '';
        }

        return (
            <div>
                {delButton}
                <Dialog
                    title={'Remove event "' + this.state.name + '" completely?'}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    autoScrollBodyContent={true}
                >
                </Dialog>
            </div>
        );
    }
}

export default withRouter(DeleteEventDialog);
