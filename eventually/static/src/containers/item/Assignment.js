import React from 'react';
import {withRouter} from 'react-router-dom'
import {getAssignment} from './ItemService.js'
const style = {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400,
    height: 270,
};

class Assignment extends React.Component {
    constructor(props) {
      super(props);
    }

    render() {
        return(
            <div style={style} >
                <h2>Assignment</h2>
                <p>{this.props.description}</p>
            </div>
        );
    };
};

export default Assignment
