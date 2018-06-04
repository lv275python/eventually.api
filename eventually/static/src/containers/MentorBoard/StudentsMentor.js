import React from 'react';
import {UsersList} from 'src/components';
import {getStudentsList, getCurriculumTopics, postStudentList} from 'src/components/studentsTabsList/studentsTabsListService';
import {isObjectsEqual} from 'src/helper';


export default class StudentsMentorList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            chosenTopic: null,
            studentsList: {
                myStudents: [],
            },
        };
    }
    componentWillMount() {
        this.getData();
    }

    getData = () => {
        const chosenTopic = this.props.title;
        this.getStudentsListData();
    };
    getStudentsListData = (chosenTopic) => {
        getStudentsList(chosenTopic)
            .then(response => {
                const data = response.data;
                this.setState({
                    studentsList: {
                        myStudents: data.my_students,
                    }
                });
            });
    };

    render() {
        return (
            <div>
                <UsersList
                    students={this.state.studentsList.myStudents}/>
            </div>
        );
    }
}
