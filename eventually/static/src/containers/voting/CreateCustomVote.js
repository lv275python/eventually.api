import React from 'react';
import Dialog from 'material-ui/Dialog';
import FlatButton from 'material-ui/FlatButton';
import TextField from 'material-ui/TextField';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
import { postVote } from './VoteService';
import { postAnswer } from './VoteService';


const FloatingButtonStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};

const regexForQuestion = /^.{5,100}\?$/;
const regexForAnswer = /^.{5,100}$/;

class CreateCustomVote extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            title: '',
            answers: {},
            textFieldsData: [
                {key: '0', id: '0', failAnswerMessage: ''},
                {key: '1', id: '1', failAnswerMessage: ''}
            ],
            failQuestionMessage: ''
        };
    }

    handleOpen = () => {
        this.setState({
            open: true,
            failQuestionMessage: ''
        });
    };

    handleClose = () => {
        this.setState({ open: false });
    };

    handleChangeQuestion = event => {
        if (regexForQuestion.test(event.target.value) === true ) {
            this.setState({
                title: event.target.value,
                failQuestionMessage: ''
            });
        } else {
            this.setState({
                failQuestionMessage: 'Question should be at least 5 symbols long and end with ? mark.'
            });
        }
    };

    handleChangeAnswer = event => {
        const textFieldId = event.target.id.toString();
        const textFieldValue = event.target.value;

        let answers = this.state.answers;
        let textFieldsData = this.state.textFieldsData;

        if (regexForAnswer.test(textFieldValue) === true ) {
            answers[textFieldId] = textFieldValue;
            textFieldsData[parseInt(textFieldId)].failAnswerMessage = '';
            this.setState({
                answers: answers,
                textFieldsData: textFieldsData
            });
        } else {
            textFieldsData[parseInt(textFieldId)].failAnswerMessage = 'Answer should be at least 5 symbols long.';
            this.setState({
                textFieldsData: textFieldsData
            });
        }
    };

    handleSubmit = event => {
        if (regexForQuestion.test(this.state.title) !== true ) {
            return;
        }
        if (Object.keys(this.state.answers).length !== this.state.textFieldsData.length) {
            return;
        }
        for (let key in this.state.answers) {
            if (regexForAnswer.test(this.state.answers[key]) !== true ) {
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
            for (var key in this.state.answers) {
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
            textFieldsData: textFieldsData
        });
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
                keyboardFocused={true}
                onClick={this.handleSubmit}
            />,
        ];
        return (
            <div>
                <FloatingActionButton
                    onClick={this.handleOpen}
                    style={FloatingButtonStyle}>
                    <ContentAdd />
                </FloatingActionButton>
                <Dialog
                    actions={actions}
                    modal={false}
                    open={this.state.open}
                    onRequestClose={this.handleClose}
                    autoScrollBodyContent={true}
                    style={{zIndex: 800}}>
                    <TextField
                        hintText="Enter question for voting:"
                        fullWidth={true}
                        errorText={this.state.failQuestionMessage}
                        onChange={this.handleChangeQuestion}/>
                    {this.getTextFields()}
                    <FlatButton
                        label="+"
                        title="Add answer"
                        primary={true}
                        onClick={this.handleAddField}
                    />
                </Dialog>
            </div>
        );
    }
}

export default CreateCustomVote;
