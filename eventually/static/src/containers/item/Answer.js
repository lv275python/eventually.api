import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import {sendAnswer} from './ItemService.js';

const style = {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400,
    height: 270,
};

class Answer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            statement:'',
        };
    }

    handleStatement = event => {
        this.setState({statement: event.target.value});
    };

    handleAnswer = event => {
        const statement = this.state.statement;
        sendAnswer(statement);
        event.preventDefault();
        alert('Your answer has been sent.');
    };

    render() {
        return(
            <div style={style} >
                <h2>Your answer</h2>
                <TextField onChange={this.handleStatement}
                    hintText='Type your answer'/>
                <br />
                <RaisedButton label='Send Answer'
                    primary={true}
                    onClick={this.handleAnswer}/>
            </div>
        );
    }
}

export default Answer;
