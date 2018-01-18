import React from 'react';
import {Tabs, Tab} from 'material-ui/Tabs';
import SwipeableViews from 'react-swipeable-views';
import UsersList from '../usersList/UsersList';
import AssignTopicModal from '../assignTopicModal/AssignTopicModal';
import {getStudentsList, getCurriculumTopics, postStudentList} from './studentsTabsListService';
import StudentsTabsFiltersBar from './StudentsTabsFiltersBar';
import {isObjectsEqual} from './helper';

export default class StudentsTabsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            slideIndex: 0,
            isModalOpen: false,
            chosenTopic: null,
            chosenStudent: null,
            isOneChosen: false,
            studentsList: {
                myStudents: [],
                allStudents: [],
                availableStudents: []
            },
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
        const chosenTopic = this.state.filtersBar.topicValue;
        const isTopicDone = this.state.filtersBar.isTopicDone;
        const fromDate = this.state.filtersBar.fromDate;
        const toDate = this.state.filtersBar.toDate;
        getStudentsList(chosenTopic, isTopicDone, fromDate, toDate)
            .then(response => {
                const data = response.data;
                console.log(data);
                this.setState({
                    studentsList: {
                        myStudents: data.my_students,
                        allStudents: data.all_students,
                        availableStudents: data.available_students
                    }
                });
            });
    }

    shouldComponentUpdate(nextProps, nextState) {

        if (!isObjectsEqual(nextState.filtersBar, this.state.filtersBar)) {
            this.getData();
            return true;
        }

        return false;
    }

    getData = () => {
        const chosenTopic = this.state.filtersBar.topicValue;
        const isTopicDone = this.state.filtersBar.isTopicDone;
        const fromDate = this.state.filtersBar.fromDate;
        const toDate = this.state.filtersBar.toDate;

        getStudentsList(chosenTopic, isTopicDone, fromDate, toDate)
            .then(response => {
                const data = response.data;
                this.setState({
                    studentsList: {
                        myStudents: data.my_students,
                        allStudents: data.all_students,
                        availableStudents: data.available_students
                    }
                });
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

    handleFiltersTopicsChange = (event, index, value) => {
        this.setState({
            filtersBar: {
                topicValue: value,
                isTopicDone: this.state.filtersBar.isTopicDone,
                fromDate: this.state.filtersBar.fromDate,
                toDate: this.state.filtersBar.toDate
            }
        });
    }

    handleFiltersFromDateChange = (event, date) => {
        this.setState({
            filtersBar: {
                topicValue: this.state.filtersBar.topicValue,
                isTopicDone: this.state.filtersBar.isTopicDone,
                fromDate: date,
                toDate: this.state.filtersBar.toDate
            }
        });
    }

    handleFiltersToDateChange = (event, date) => {
        this.setState({
            filtersBar: {
                topicValue: this.state.filtersBar.topicValue,
                isTopicDone: this.state.filtersBar.isTopicDone,
                fromDate: this.state.filtersBar.from,
                toDate: date
            }
        });
    }

    handleFiltersIsDoneToggle = (event, isInputChecked) => {
        this.setState({
            filtersBar: {
                topicValue: this.state.filtersBar.topicValue,
                isTopicDone: isInputChecked,
                fromDate: this.state.filtersBar.from,
                toDate: this.state.filtersBar.toDate
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
                            students={this.state.studentsList.myStudents}
                            onItemButtonClick={this.handleModalOpen}
                            tabIndex={this.state.slideIndex}
                        />
                    </div>
                    <div>
                        <UsersList
                            students={this.state.studentsList.allStudents}
                            onItemButtonClick={this.handleModalOpen}
                            tabIndex={this.state.slideIndex}
                        />
                    </div>
                    <div>
                        <UsersList
                            students={this.state.studentsList.availableStudents}
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
