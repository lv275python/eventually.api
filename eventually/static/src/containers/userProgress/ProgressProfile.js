import React from 'react';
import {ItemsList, MessagesBar, ProgressGraph, GraphProgress, TeamList, CurriculumList} from 'src/containers';
import Menu from 'material-ui/Menu';
import MenuItem from 'material-ui/MenuItem';
import Paper from 'material-ui/Paper';
import TimeLine from 'material-ui/svg-icons/action/timeline';
import Group from 'material-ui/svg-icons/social/group';
import List from 'material-ui/svg-icons/action/list';
import Divider from 'material-ui/Divider';
import {lightBlueA700} from 'material-ui/styles/colors';
import AssignmentCurriculumList from 'src/containers/assignment/AssignmentCurriculumList';

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

const itemsGraphWrapperStyle = {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    width: '70%'
};

const itemsGraphStyle = {
    paddingTop: 10,
    width: '90%',
    maxWidth: '90%'
};

const messagesBarStyle = {
    width: '30%',
    position: 'relative'
};

const teamListStyle = {
    display: 'block',
    flexWrap: 'wrap',
    flexDirection: 'column',
    width: '50%',
    maxWidth: '50%',
    minWidth: '50%',

};

export default class ProgressProfile extends React.Component {

    goToUserProfile = (id) => {
        this.props.history.push('/profile/' + id);
    };

    constructor(props) {
        super(props);
        this.state = {
            'currentPage': <TeamList style={teamListStyle} goToUserProfile={this.goToUserProfile}/>
        };
    }

    render() {
        return (
            <div style={generalStyle}>
                <Paper zDepth={2} style={userProgressStyle}>
                    <Menu>
                        <MenuItem primaryText="Teams" leftIcon={<Group color={lightBlueA700}/>}
                            onClick={() => this.setState({
                                currentPage: <TeamList style={teamListStyle}
                                    goToUserProfile={this.goToUserProfile}/>})}
                        />
                        <Divider/>
                        <MenuItem primaryText="Progress chart" leftIcon={<TimeLine color={lightBlueA700}/>}
                            onClick={() => this.setState({currentPage: <GraphProgress/>})}/>
                        <Divider/>
                        <MenuItem primaryText="Assignments" leftIcon={<List color={lightBlueA700}/>}
                            onClick={() => this.setState({
                                currentPage: <AssignmentCurriculumList
                                />})}
                        />
                    </Menu>
                </Paper>
                <div style={teamListStyle}>
                    {this.state.currentPage}
                </div>
                <MessagesBar
                    style={messagesBarStyle}
                    location={this.props.location.pathname.slice(1)}
                    expandedWidth={'30%'}
                    wrappedWidth={'5%'}
                    type='student'
                />
            </div>);
    }
}
