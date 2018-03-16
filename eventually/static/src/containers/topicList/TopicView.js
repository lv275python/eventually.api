import React from 'react';
import { withRouter } from 'react-router-dom';
import {red500, blue300} from 'material-ui/styles/colors';
import Avatar from 'material-ui/Avatar';
import SvgIcon from 'material-ui/SvgIcon';
import DeleteForever from 'material-ui/svg-icons/action/delete-forever';
import ModeEdit from 'material-ui/svg-icons/editor/mode-edit';
import Chip from 'material-ui/Chip';
import Dialog from 'material-ui/Dialog';
import FloatingActionButton from 'material-ui/FloatingActionButton';
import ContentAdd from 'material-ui/svg-icons/content/add';
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
    getIsMentorService,
    EditTopicDialog
} from 'src/containers';


const wrapperButtonStyle = {
    display: 'flex',
    justifyContent: 'space-between'
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
    flexWrap: 'wrap'
};

const chipStyle = {
    margin: 4,
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
        this.getTopicData();
    }

    getTopicData = () => {
        getTopicDetailService(this.state.curriculumId, this.state.topicId).then(response => {
            return response.data;
        }).then(data => {
            this.setState({'topicDetail': data, 'mentorsDetail': []});
            data['mentors'].map(mentorId => (
                getProfileService(mentorId).then(response => {
                    let mentorsDetail = this.state.mentorsDetail;
                    mentorsDetail.push(response.data);
                    this.setState(mentorsDetail);
                })
            ));
        });
    };

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
        if (this.state.isMentor && this.state.topicDetail){
            cardActions = [
                <RaisedButton
                    key={1}
                    icon={<DeleteForever color={red500} />}
                    onClick={this.handleDelete} />,
                <EditTopicDialog
                    key={0}
                    topicId={this.state.topicId}
                    curriculumId={this.state.curriculumId}
                    topicDetail={this.state.topicDetail}
                    getTopicData={this.getTopicData} />
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
                    <CardActions style={wrapperButtonStyle}>
                        {cardActions}
                    </CardActions>
                    <CardTitle
                        title={this.state.topicDetail['title']}
                        subtitle={this.state.topicDetail['description']} />
                    <div style={wrapperStyle}>
                        {this.state.mentorsDetail.map(mentor => (
                            <MentorsChip
                                id={mentor['user']}
                                key={mentor['user']}
                                style={chipStyle}
                                photo={getImageUrl(mentor['photo'])}
                                text={'Mentor ' + mentor['first_name'] + ' ' + mentor['last_name']} />
                        ))}
                        {this.state.isMentor && (<Chip
                            style={chipStyle}
                            onClick={this.handleAddMentor}
                        >
                            <Avatar backgroundColor={blue300} icon={<ContentAdd />} />
                            Add mentor
                        </Chip>)}
                    </div>
                    <CardHeader
                        title='Course materials'
                        subtitle='You have to pass these materials in order in which they are appear below' />
                    <TopicItemList
                        curriculumId={this.state.curriculumId}
                        topicId={this.state.topicId}
                        isMentor={this.state.isMentor} />
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
