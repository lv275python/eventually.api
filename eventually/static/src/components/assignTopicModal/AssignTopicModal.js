import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import AssignTopicItem from './AssignTopicItem';

export default class AssignTopicModal extends React.Component {

    constructor(props) {
        super(props);
    }

    handleTopicCheck = this.props.onTopicCheck;
    handleCancelClick = this.props.onCancelClick;

    render() {

        const actions = [];

        const cancelButton = (
            <FlatButton
                label="Cancel"
                secondary={true}
                onClick={this.handleCancelClick}
            />);

        let submitButton;

        if (this.props.isOneChosen) {

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
                    <h3>Please, choose one of the available topics</h3>
                    <div>
                        {
                            this.props.topics.map(topic => (
                                <AssignTopicItem 
                                    key={topic.id.toString()}
                                    id={topic.id}
                                    title={topic.title}
                                    onCheck={this.handleTopicCheck}
                                />
                            ))
                        }
                    </div>
                </Dialog>
            </div>
        );
    }
}
