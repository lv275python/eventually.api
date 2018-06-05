import React from 'react';
import {getStudentsList} from 'src/components/studentsTabsList/studentsTabsListService';
import {isObjectsEqual} from 'src/helper';
import {Card} from 'material-ui/Card';
import StudentList from './StudentList';


export default class StudentsMentorList extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            studentsList: {
                myStudents: [],
            },
        };
    }
    componentWillMount() {
        this.getData();
    }

    getData = () => {
        this.getStudentsListData(this.props.id, false);
    };
    getStudentsListData = (chosenTopic, isTopicDone) => {
        getStudentsList(chosenTopic, isTopicDone)
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
            <Card>
                <StudentList
                    curriculumId = {this.props.curriculumId}
                    students={this.state.studentsList.myStudents}/>
            </Card>
        );
    }
}
