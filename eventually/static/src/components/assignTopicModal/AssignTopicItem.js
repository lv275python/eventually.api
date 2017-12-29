import React from 'react';
import Checkbox from 'material-ui/Checkbox';

const checkBoxStyles = {
    marginBottom: 16
};


export default class AssignTopicItem extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            checked: false
        };
    }
    
    handleCheck = (event, isInputChecked) => {
        this.props.onCheck(this.props.id, isInputChecked);
    };

    render() {
        return (
            <Checkbox
                key={this.props.id}
                label={this.props.title}
                style={checkBoxStyles}
                onCheck={this.handleCheck}
            />
        );
    }
}
