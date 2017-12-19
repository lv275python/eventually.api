import React from 'react';
import LinearProgress from 'material-ui/LinearProgress';
import {lightGreen500} from 'material-ui/styles/colors';

const style = {
    height: 23,
    borderRadius: 8
};

export default class Progress extends React.Component {

    constructor(props) {
        super(props);

        this.state = {
            completed: 10,
            max: 20,
            min: 0,
        };
    }

    progress(completed, max) {
        if (completed > max) {
            this.setState({completed: max});
        } else {
            this.setState({completed});
        }
    }

    render() {
        return (
            <div>
                <LinearProgress mode="determinate"
                    min={this.state.min}
                    max={this.state.max}
                    style={style}
                    color={lightGreen500}
                    value={this.state.completed}/>
            </div>
        );
    }
}
