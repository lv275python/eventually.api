import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import SwipeableViews from 'react-swipeable-views';
import UsersList from '../usersList/UsersList';
import AssignTopicModal from '../assignTopicModal/AssignTopicModal';
import { getStudentsList, getCurriculumTopics, postStudentList} from './studentsTabsListService';
import StudentsTabsFiltersBar from './StudentsTabsFiltersBar';

export default class StudentsTabsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            slideIndex: 0,
            isModalOpen: false,
            chosenTopic: null,
            chosenStudent: null,
            isOneChosen: false,
            studentsList: null,
            curriculumTopics: null,
            filtersBar: {
                topicValue: null,
                isTopicDone: false,
                fromDate: null,
                toDate: null
            }
        };
    }

    componentWillMount() {
        this.setState({
            studentsList: getStudentsList(),
            curriculumTopics: getCurriculumTopics()
        });
    }

    handleChange = (value) => {
        this.setState({
            slideIndex: value
        });
    };

    handleModalOpen = (studentId) => {
        this.setState({
            isModalOpen: true,
            chosenStudent: studentId
        });
    };

    handleModalClose = () => {
        this.setState({
            isModalOpen: false,
            isOneChosen: false,
            chosenStudent: null,
            chosenTopic: null,
        });
    };

    handleTopicCheck = (event, topicId) => {
        this.setState({
            chosenTopic: topicId,
            isOneChosen: true
        });
    };

    handleTopicsSubmit = () => {
        postStudentList(this.state.chosenStudent, this.state.chosenTopic)
            .then(response => {
                this.handleModalClose();
            });
    }

    handleFilterBarChange = (filterParameters) => {
        const chosenTopic = filterParameters.chosenTopic;
        const isTopicDone = filterParameters.isTopicDone;
        const fromDate = filterParameters.fromDate;
        const toDate = filterParameters.toDate;

        getStudentsList(chosenTopic, isTopicDone, fromDate, toDate)
            .then((response) => {
                const data = response.data;
                this.setState({
                    studentsList: data.students
                });
            });
    }

    handleFiltersTopicsChange = (event, index, value) => {
        this.setState({
            filtersBar: {
                topicValue: value
            }
        });
    }

    handleFiltersFromDateChange = (event, date) => {
        this.setState({
            filtersBar: {
                fromDate: date
            }
        });
    }

    handleFiltersToDateChange = (event, date) => {
        this.setState({
            filtersBar: {
                toDate: date
            }
        });
    }

    handleFiltersIsDoneToggle = (event, isInputChecked) => {
        this.setState({
            filtersBar: {
                isTopicDone: isInputChecked
            }
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
                <StudentsTabsFiltersBar 
                    topicValue={this.state.filtersBar.topicValue}
                    fromDate={this.state.filtersBar.fromDate}
                    toDate={this.state.filtersBar.toDate}
                    onFiltersTopicsChange={this.handleFiltersTopicsChange}
                    onFiltersFromDateChange={this.handleFiltersFromDateChange}
                    onFiltersToDateChange={this.handleFiltersToDateChange}
                    onFiltersIsDoneToggle={this.handleFiltersIsDoneToggle}
                />
                <SwipeableViews
                    index={this.state.slideIndex}
                    onChangeIndex={this.handleChange}
                    style={{margin: 5}}
                >
                    <div>
                        <UsersList
                            students={this.state.studentsList}
                            onItemButtonClick={this.handleModalOpen}
                            tabIndex={this.state.slideIndex}
                        />
                    </div>
                    <div>
                        <UsersList 
                            students={this.state.studentsList}
                            onItemButtonClick={this.handleModalOpen}
                            tabIndex={this.state.slideIndex}
                        />
                    </div>
                    <div>
                        <UsersList
                            students={this.state.studentsList}
                            onItemButtonClick={this.handleModalOpen}
                            tabIndex={this.state.slideIndex}
                        />
                    </div>
                </SwipeableViews>
                <AssignTopicModal 
                    isModalOpen={this.state.isModalOpen} 
                    onCancelClick={this.handleModalClose}
                    onSubmitClick={this.handleTopicsSubmit} 
                    topics={this.state.curriculumTopics}
                    onTopicCheck={this.handleTopicCheck}
                    isOneChosen={this.state.isOneChosen}/>
            </div>
        );
    }
}
