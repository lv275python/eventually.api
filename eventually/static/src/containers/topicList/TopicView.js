import React from 'react';
import { withRouter } from 'react-router-dom';
import Dialog from 'material-ui/Dialog';
import RaisedButton from 'material-ui/RaisedButton';
import FlatButton from 'material-ui/FlatButton';
import { Card, CardActions, CardHeader, CardMedia, CardTitle, CardText } from 'material-ui/Card';
import { lightGreen400 } from 'material-ui/styles/colors';
import { getUserId } from 'src/helper';
import { getImageUrl } from 'src/helper';
import {
    deleteTopicService,
    getTopicDetailService,
    getProfileService,
    TopicItemList,
    MentorsChip,
    getIsMentorService
} from 'src/containers';


const wrapperButtonStyle = {
    display: 'flex',
    justifyContent: 'flex-end',
};

const cardTextStyle = {
    color: '#455A64',
    fontSize: '15px'
};

const cardHeaderStyle= {
    fontSize: '25px'
};

const style = {
    width: '80%',
    margin: '0 auto',
    paddingBottom: '20px',
};

const wrapperStyle = {
    display: 'flex',
    flexWrap: 'wrap',
};

class TopicView extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            curriculumId: this.props.match.params.curriculumId,
            topicId: this.props.match.params.topicId,
            topicDetail: {},
            mentorsDetail: [],
            isMentor: false,
            deleteDialogOpen: false
        };
    }

    componentWillMount(){
        getIsMentorService(this.state.curriculumId, this.state.topicId).then(response => {
            this.setState({isMentor: response.data['is_mentor']});
        });
        getTopicDetailService(this.state.curriculumId, this.state.topicId).then(response => {
            return response.data;
        }).then(data => {
            this.setState({'topicDetail': data});
            data['mentors'].map(mentorId => (
                getProfileService(mentorId).then(response => {
                    let mentorsDetail = this.state.mentorsDetail;
                    mentorsDetail.push(response.data);
                    this.setState(mentorsDetail);
                })
            ));
        });
    }

    handleDelete = () => {
        this.handleOpen();
    };

    handleOpen = () => {
        this.setState({ deleteDialogOpen: true });
    };

    handleClose = () => {
        this.setState({ deleteDialogOpen: false });
    };

    handleYes = () => {
        deleteTopicService (this.state.curriculumId, this.state.topicId).then(response => {
            this.props.history.push('/curriculums/');
        });
    };

    handleNo = () => {
        this.handleClose();
    };

    render() {
        let cardActions;
        if (this.state.isMentor){
            cardActions = [
                <RaisedButton
                    label='Delete topic'
                    backgroundColor="#D50000"
                    labelColor="#FFF"
                    key={0}
                    onClick={this.handleDelete} />,
                <RaisedButton
                    label='Edit topic'
                    key={1}
                    onClick={this.handleEdit} />
            ];
        } else {
            cardActions = [];
        }

        const actionsDialog = [
            <FlatButton
                label="Yes"
                key={1}
                primary={true}
                onClick={this.handleYes}
            />,
            <FlatButton
                label="No"
                key={0}
                primary={true}
                onClick={this.handleNo}
            />

        ];

        return (
            <div style={style}>
                <Card>
                    <div style={wrapperButtonStyle}>
                        <CardActions>
                            {cardActions}
                        </CardActions>
                    </div>
                    <CardTitle
                        title={this.state.topicDetail['title']}
                        subtitle={this.state.topicDetail['description']} />
                    <div style={wrapperStyle}>
                        {this.state.mentorsDetail.map(mentor => (
                            <MentorsChip
                                id={mentor['user']}
                                key={mentor['user']}
                                photo={getImageUrl(mentor['photo'])}
                                text={'Mentor ' + mentor['first_name'] + ' ' + mentor['last_name']} />
                        ))}
                    </div>
                    <CardHeader
                        title='Course materials'
                        subtitle='You have to pass these materials in order in which they are appear below' />
                    <TopicItemList
                        curriculumId={this.state.curriculumId}
                        topicId={this.state.topicId} />
                    <Dialog
                        actions={actionsDialog}
                        modal={true}
                        open={this.state.deleteDialogOpen}
                    >
                        Do you really want to delete topic?
                    </Dialog>
                </Card>
            </div>
        );
    }
}

export default withRouter(TopicView);
