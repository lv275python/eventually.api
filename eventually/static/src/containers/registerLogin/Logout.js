import React from 'react';
import {withRouter} from 'react-router-dom';
import RaisedButton from 'material-ui/RaisedButton';
import {logoutService} from './registrationService.js';

const style = {
    margin: 12,
};

class Logout extends React.Component {

    constructor(props) {
        super(props);
    }

    handleSubmit = event => {
        logoutService().then(response => this.props.history.push('/home'));
    };

    render() {
        return (
            <div style={style}>
                <RaisedButton
                    label='Logout'
                    primary={true}
                    onClick={this.handleSubmit}
                />
            </div>
        );
    }
}

export default withRouter(Logout);
