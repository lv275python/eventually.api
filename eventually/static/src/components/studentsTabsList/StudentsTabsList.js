import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import SwipeableViews from 'react-swipeable-views';
import UsersList from '../usersList/UsersList';
import AssignTopicModal from '../assignTopicModal/AssignTopicModal';
import {getAllStudentsList, getAvailableStudentsList, getMentorStudentsList, getCurriculumTopics} from './studentsTabsListService';

export default class StudentsTabsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            slideIndex: 0,
            isModalOpen: false,
            chosenTopics: [],
            isOneChosen: false
        };
    }

    handleChange = (value) => {
        this.setState({
            slideIndex: value
        });
    };

    handleModalOpen = () => {
        this.setState({isModalOpen: true});
    };

    handleModalClose = () => {
        this.setState({
            isModalOpen: false,
            isOneChosen: false
        });
    };

    handleTopicCheck = (topicId, isInputChecked) => {
        let chosenTopics = this.state.chosenTopics.slice();

        if (isInputChecked) {
            chosenTopics.push(topicId);
        } else {
            chosenTopics.pop(topicId);
        }

        this.setState({
            chosenTopics: chosenTopics,
            isOneChosen: chosenTopics.length
        });
    };

    componentWillMount() {
        this.setState({
            mentorStudents: getMentorStudentsList(),
            allStudents: getAllStudentsList(),
            availableStudents: getAvailableStudentsList(),
            curriculumTopics: getCurriculumTopics()
        });
    }

    render() {
        return (
            <div style={this.props.style}>
                <Tabs
                    onChange={this.handleChange}
                    value={this.state.slideIndex}
                >
                    <Tab label="My students" value={0} />
                    <Tab label="All students" value={1} />
                    <Tab label="Available students" value={2} />
                </Tabs>
                <SwipeableViews
                    index={this.state.slideIndex}
                    onChangeIndex={this.handleChange}
                >
                    <div>
                        <UsersList
                            students={this.state.mentorStudents}
                            onItemButtonClick={this.handleModalOpen}
                        />
                    </div>
                    <div>
                        <UsersList 
                            students={this.state.allStudents}
                            onItemButtonClick={this.handleModalOpen}
                        />
                    </div>
                    <div>
                        <UsersList
                            students={this.state.availableStudents}
                            onItemButtonClick={this.handleModalOpen}
                        />
                    </div>
                </SwipeableViews>
                <AssignTopicModal 
                    isModalOpen={this.state.isModalOpen} 
                    onCancelClick={this.handleModalClose} 
                    topics={this.state.curriculumTopics}
                    onTopicCheck={this.handleTopicCheck}
                    isOneChosen={this.state.isOneChosen}/>
            </div>
        );
    }
}
