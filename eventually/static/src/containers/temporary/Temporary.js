import React from 'react';
import { Link } from 'react-router';
import { withRouter } from 'react-router-dom';

class Temporary extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            temporary: false
        };
    }

    componentWillMount() {
        this.setState({
            temporary: true
        });
    }

    render() {
        return (
          <div>Hello</div>
        );
    }
}
export default Temporary;
