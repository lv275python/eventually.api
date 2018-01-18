import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import {RadioButton, RadioButtonGroup} from 'material-ui/RadioButton';

export default class AssignTopicModal extends React.Component {

    constructor(props) {
        super(props);
    }

    handleCancelClick = this.props.onCancelClick;
    handleSubmitClick = this.props.onSubmitClick;
    handleRadioButtonChange = (event, value) => {
        this.props.onTopicCheck(event, value);
    };

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
                    onClick={this.handleSubmitClick}
                />);

        } else {

            submitButton = (
                <FlatButton
                    label="Submit"
                    primary={true}
                    disabled={true}
                    onClick={this.handleSubmitClick}
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
                        <RadioButtonGroup 
                            name='topics'
                            onChange={this.handleRadioButtonChange}
                        >
                            {this.props.topics.map(topic => (
                                <RadioButton
                                    key={topic.id}
                                    value={topic.id}
                                    label={topic.title}
                                />
                            ))}
                        </RadioButtonGroup>
                    </div>
                </Dialog>
            </div>
        );
    }
}
