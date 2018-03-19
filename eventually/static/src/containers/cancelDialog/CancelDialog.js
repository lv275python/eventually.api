import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';


export default class CancelDialog extends React.Component {
    constructor(props) {
        super(props);
    }

    handleDialogClose = () => {
        this.props.handleCancelMainDialogClose();
    }

    handleRequestClose = event => {
        this.props.handleCancelDialogClose();
    };

    render() {
        const actions = [
            <FlatButton
                label="Close"
                primary={true}
                onClick={this.handleDialogClose}
            />,
            <FlatButton
                label="Continue"
                primary={true}
                onClick={this.handleRequestClose}
            />,
        ];
        return (
            <div>
                <Dialog
                    title="Confirm action"
                    actions={actions}
                    modal={true}
                    open={this.props.openCancelDialog}
                    autoDetectWindowHeight={true}
                >
                    Close dialog without saving or continue editing?
                </Dialog>
            </div>
        );
    }
}
