import React from 'react';
import {MessagesBar, ProgressGraph} from 'src/containers';
import {StudentsTabsList} from 'src/components';
import Paper from 'material-ui/Paper';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import Divider from 'material-ui/Divider';
import MentorBoard from '../MentorBoard/MentorBoard';


const mentorDashboardStyle = {
    display: 'flex',
    justifyContent: 'space-between'
};

const userProgressStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'stretch',
    height: '30%',
    margin: '1%',
};

const generalStyle =
    {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'stretch'
    };



const usersListGraphWrapperStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '70%'
};

const usersListStyle = {
    width: '95%',
    maxWidth: '95%'
};

const progressGraphStyle = {
    width: '85%',
    maxWidth: '85%'
};

const messagesBarStyle = {
    width: '30%',
    position: 'relative'
};

export default class MentorDashboard extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            'currentPage': <MentorBoard/>,
        };
    }

    render() {
        return (
            <div style={generalStyle}>
                <Paper  zDepth={2} style={userProgressStyle}>
                    <Menu>
                        <MenuItem primaryText='Mentor Board'
                            onClick={() => this.setState({currentPage: <MentorBoard
                            />})}/>
                        <Divider/>
                        <MenuItem primaryText='My Students'
                            onClick={() => this.setState({ currentPage: <div>
                                <ProgressGraph style={progressGraphStyle} />
                                <StudentsTabsList style={usersListStyle} />
                            </div> })}
                        />
                    </Menu>
                </Paper>
                <div style={usersListGraphWrapperStyle}>
                    {this.state.currentPage}
                </div>

                <MessagesBar
                    style={messagesBarStyle}
                    location={this.props.location.pathname.slice(1)}
                    expandedWidth={'30%'}
                    wrappedWidth={'5%'}
                    type='mentor'
                />
            </div>
        );
    }
}
