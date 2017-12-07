import React from 'react';
import {List, ListItem} from 'material-ui/List';
import ContentInbox from 'material-ui/svg-icons/content/inbox';
import ActionGrade from 'material-ui/svg-icons/action/grade';
import ContentSend from 'material-ui/svg-icons/content/send';
import Subheader from 'material-ui/Subheader';
import TopicsList from '../topicList/TopicList';
import MentorsList from './MentorsList';
import {mentorsService} from './CurriculumService';

const style_h3={
    marginLeft:30,
}

const style_left_div={
    float:'left',
    width:'70%',
    minWidth: 330,
}

const style_right_div={
    float:'left',
    width:'30%',
    minWidth: 140,
}

const main_style={
    float: 'left',
    width: '100%',
    fontFamily: 'Roboto, sans-serif',
}

const style={
    fontSize: '1.25em',
}

const style_header={
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
}

const style_p={
    clear: 'both',
    marginLeft: 30,
    marginRight: 30,
    textAlign: 'justify',
    color: 'rgba(0, 0, 0, 0.54)',
}

export default class Curriculum extends React.Component {

    constructor(props) {
        super(props);
    }

    componentWillMount() {
        this.setState({
            mentors: mentorsService().mentors
        })
    }

    render() {
        return (
        <div style={main_style}>
            <div style={style_left_div}>
                <div style={style_header}>
                  <h1>Curriculum Name</h1>
                  <h3 style={style_h3}>here should be the goal of the curriculum</h3>
                </div>
                <p style={style_p}>
                Lorem ipsum dolor sit amet, consectetur adipiscing elit. Vestibulum eu mattis eros. Proin venenatis faucibus dictum. Ut tristique convallis ligula, ut porta sapien fringilla at. Phasellus massa nibh, vulputate eget rhoncus vel, consequat sit amet elit. Quisque tristique sodales neque nec viverra. Curabitur molestie lectus id mauris commodo malesuada. Ut semper enim id tortor ullamcorper, eget efficitur sapien faucibus. Nam quis lorem vel augue tempus facilisis id id est. Nullam ac augue ante.
                </p>
                <div>
                    <TopicsList />
                </div>
            </div>
            <div style={style_right_div}>
                <Subheader style={style}>Your mentors</Subheader>
                <MentorsList mentors={this.state.mentors}/>
            </div>
        </div>
        )
    }
}
