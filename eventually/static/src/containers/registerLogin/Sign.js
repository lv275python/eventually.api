import React from 'react';
import {withRouter} from 'react-router-dom';
import {Tab, Tabs} from 'material-ui/Tabs';


class Sign extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            value: props.history.location.pathname.split('/')[1],
        };
    }

    handleChange = (value) => {
        this.setState({
            value: value,
        });
    };

    toRegister = () => {
        this.props.history.push('/register');
    };

    toLogin = () => {
        this.props.history.push('/login');
    };

    toForgetPassword = () => {
        this.props.history.push('/forget');
    };

    render() {
        return (
            <Tabs onChange={this.handleChange}
                value={this.state.value}
            >
                <Tab label='Register' value ='register' onActive={this.toRegister}>
                </Tab>
                <Tab label='Login' value ='login' onActive={this.toLogin}>
                </Tab>
                <Tab label='Forget password' value ='forget' onActive={this.toForgetPassword}>
                </Tab>
            </Tabs>

        );
    }
}

export default withRouter(Sign);
