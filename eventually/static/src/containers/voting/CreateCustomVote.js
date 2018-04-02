import React from 'react';
import ContentAdd from 'material-ui/svg-icons/content/add';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import { CancelDialog } from 'src/containers';
import { postVote, postAnswer } from './VoteService';


const styles = {
    raisedButton: {
        minWidth: 20,
        width: 40,
        marginRight: 10
    },
    dialog: {
        zIndex: 800
    },
    dialogContent: {
        width: '50%',
        minWidth: 400
    },
    floatingButton: {
        position: 'fixed',
        right: '3%',
        top: '85%'
    },
    fieldSet: {
        marginBottom: '10px',
        borderRadius: '5px',
        border: '1px solid #12bbd2'
    },
    legend: {
        fontWeight: 'bold'
    }
};

const regexForQuestion = /^.{5,100}\?$/;
const regexForAnswer = /^.{5,100}$/;
const failQuestionMessage = 'Question should be at least 5 symbols long and end with ? mark.';
const failAnswerMessage = 'Answer should be at least 5 symbols long.';

class CreateCustomVote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            title: '',
            answers: {},
            textFieldsData: [],
            failQuestionMessage: '',
            openCancelDialog: false,
            disabled: true
        };
    }

    handleOpen = () => {
        this.setState({
            open: true,
            title: '',
            failQuestionMessage: '',
            answers: {},
            textFieldsData: [
                {key: '0', id: '0', failAnswerMessage: ''},
                {key: '1', id: '1', failAnswerMessage: ''}
            ]
        });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    handleChangeQuestion = event => {
        if (this.isValidQuestion(event.target.value)) {
            this.setState({
                title: event.target.value,
                failQuestionMessage: '',
                disabled: this.isEveryTextfieldFilledWithAnswer() ? false : true
            });
        } else {
            this.setState({
                title: event.target.value,
                failQuestionMessage: failQuestionMessage,
                disabled: true
            });
        }
    };

    handleChangeAnswer = event => {
        const textFieldId = event.target.id.toString();
        const textFieldValue = event.target.value;

        let answers = this.state.answers;
        let textFieldsData = this.state.textFieldsData;

        if (this.isValidAnswer(textFieldValue)) {
            answers[textFieldId] = textFieldValue;
            textFieldsData[parseInt(textFieldId)].failAnswerMessage = '';
            this.setState({
                answers: answers,
                textFieldsData: textFieldsData,
                disabled: this.isEveryTextfieldFilledWithAnswer() ? false : true
            });
        } else {
            textFieldsData[parseInt(textFieldId)].failAnswerMessage = failAnswerMessage;
            delete answers[textFieldId];
            this.setState({
                answers: answers,
                textFieldsData: textFieldsData,
                disabled: true
            });
        }
    };

    handleSubmit = event => {
        if (!this.isValidQuestion(this.state.title)) {
            return;
        }
        if (!this.isEveryTextfieldFilledWithAnswer()) {
            return;
        }
        for (let key in this.state.answers) {
            if (!this.isValidAnswer(this.state.answers[key])) {
                return;
            }
        }
        const title = {
            'title': this.state.title,
            'event': parseInt(this.props.event)
        };
        this.PostVoteService(title);
        this.handleClose();
    };

    PostVoteService = (data) => {
        postVote(data).then(response => {
            const vote = response.data;
            vote['answers'] = [];
            this.props.addVote(vote);
            for (let key in this.state.answers) {
                postAnswer(
                    this.state.answers[key],
                    parseInt(this.props.event),
                    response.data.id
                ).then(response => {
                    vote['answers'].push(response.data);
                    this.props.addAnswer(vote);
                });
            }
        });
    };

    getTextFields() {
        return this.state.textFieldsData.map(field => {
            return <TextField
                key={field.key}
                hintText="Enter possible answer:"
                errorText={this.state.textFieldsData[parseInt(field.id)].failAnswerMessage}
                fullWidth={true}
                id={field.id}
                onChange={this.handleChangeAnswer}
            />;
        });
    }

    handleAddField = event => {
        const index = this.state.textFieldsData.length.toString();
        let textFieldsData = this.state.textFieldsData;
        textFieldsData.push({
            key: index,
            id: index
        });
        this.setState({
            textFieldsData: textFieldsData,
            disabled: true
        });
    };

    handleRemoveField = event => {
        let textFieldsData = this.state.textFieldsData;
        let answers = this.state.answers;
        textFieldsData.pop();
        delete answers[(textFieldsData.length).toString()];
        this.setState({
            textFieldsData: textFieldsData,
            answers: answers,
            disabled: false
        });
    };

    handleCancelDialogClose = () => {
        this.setState({'openCancelDialog': false});
    };

    handleCancelCreateDialogClose = () => {
        this.handleCancelDialogClose();
        this.handleClose();
    };

    handleRequestClose = () => {
        if ((this.state.title != '') ||
            (this.state.answers.length > 0)) {
            this.setState({openCancelDialog: true});
        }
        else this.handleClose();
    };

    isValidQuestion = question => {
        return regexForQuestion.test(question) === true;
    };

    isValidAnswer = answer => {
        return regexForAnswer.test(answer) === true;
    };

    isEveryTextfieldFilledWithAnswer = () => {
        const answersLength = Object.keys(this.state.answers).length;
        return answersLength === this.state.textFieldsData.length;
    };

    isSubmitDisabled = () => {
        if (this.isValidQuestion(this.state.title) && this.isEveryTextfieldFilledWithAnswer()) {
            return this.state.disabled;
        } else {
            return true;
        }
    };

    render() {
        const actions = [
            <FlatButton
                label="Cancel"
                primary={true}
                onClick={this.handleClose}
            />,
            <FlatButton
                label="Submit"
                primary={true}
                disabled={this.isSubmitDisabled()}
                keyboardFocused={true}
                onClick={this.handleSubmit}
            />
        ];
        return (
            <div>
                <FloatingActionButton
                    onClick={this.handleOpen}
                    style={styles.floatingButton}
                    disabled={this.props.disabled}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    contentStyle={styles.dialogContent}
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleRequestClose}
                    autoScrollBodyContent={true}
                    style={styles.dialog}>
                    <fieldset style={styles.fieldSet}>
                        <legend style={styles.legend}>Input question</legend>
                        <TextField
                            hintText="Enter question for voting:"
                            fullWidth={true}
                            errorText={this.state.failQuestionMessage}
                            onChange={this.handleChangeQuestion}/>
                    </fieldset>
                    <fieldset style={styles.fieldSet}>
                        <legend style={styles.legend}>Input answers</legend>
                        {this.getTextFields()}
                    </fieldset>
                    <RaisedButton
                        style={styles.raisedButton}
                        label="+"
                        title="Add answer"
                        primary={true}
                        disabled={this.state.textFieldsData.length == 5 ? true : false}
                        onClick={this.handleAddField}
                    />
                    <RaisedButton
                        style={styles.raisedButton}
                        label="-"
                        title="Remove answer"
                        primary={true}
                        disabled={this.state.textFieldsData.length <= 2 ? true : false}
                        onClick={this.handleRemoveField}
                    />
                </Dialog>
                {this.state.openCancelDialog &&
                    (<CancelDialog
                        openCancelDialog={this.state.openCancelDialog}
                        handleCancelMainDialogClose={this.handleCancelCreateDialogClose}
                        handleCancelDialogClose={this.handleCancelDialogClose}
                    />)
                }
            </div>
        );
    }
}

export default CreateCustomVote;
