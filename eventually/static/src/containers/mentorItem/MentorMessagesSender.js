import React from 'react';
import TextField from 'material-ui/TextField';
import RaisedButton from 'material-ui/RaisedButton';
import Paper from 'material-ui/Paper';

const paperStyle = {
    'marginTop': 10,
    'marginBottom': 10,
    'padding': 10,
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'flex-start'
};

const buttonStyle = {
    alignSelf: 'flex-end'
};

export default class MentorMessagesSender extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {

        return (
            <div>
                <Paper style={paperStyle} zDepth={2}>
                    <TextField
                        fullWidth={true}
                        multiLine={true}
                        rowsMax={8}
                        hintText="Enter your message"
                    />
                    <RaisedButton label="Send" primary={true} style={buttonStyle}/>
                </Paper>
            </div>
        );
    }
}
