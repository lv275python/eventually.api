import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';


export default class SendAnswer extends React.Component {

    constructor(props) {
        super(props);
    }

    handleChange = this.props.onAnswerChange;

    render() {

        const actions = [];

        const cancelButton = (
            <FlatButton
                label="Cancel"
                secondary={true}
                onClick={this.props.onModalClose}
            />);

        let submitButton;

        if (this.props.answer) {

            submitButton = (
                <FlatButton
                    label="Submit"
                    primary={true}
                    disabled={false}
                    onClick={this.handleClose}
                />);

        } else {

            submitButton = (
                <FlatButton
                    label="Submit"
                    primary={true}
                    disabled={true}
                    onClick={this.handleClose}
                />);
        }

        actions.push(cancelButton, submitButton);

        return (
            <div>
                <Dialog
                    actions={actions}
                    modal={true}
                    open={this.props.isModalOpen}
                >
                    <TextField
                        fullWidth={true}
                        multiLine={true}
                        rowsMax={10}
                        hintText='Please, write your answer here...'
                        value={this.props.answer}
                        onChange={this.handleChange}
                    />
                </Dialog>
            </div>
        );
    }
}
