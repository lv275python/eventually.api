import React from 'react';
import MentorTopicLink from './MentorTopicLink';


const style = {
    width: '80%',
    margin: '0 auto',
    paddingBottom: '20px',
};

export default class MentorList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            topics: props.topics,
            isActive: -1
        };
    }

    componentWillReceiveProps(nextProps){
        if(this.props.topics !== nextProps.topics){
            this.setState({
                topics: nextProps.topics
            });
        }
    }

    change = id => {
        if (this.state.isActive === id) {
            this.setState({isActive: -1});
        } else {
            this.setState({isActive: id});
        }
    };

    render() {

        return (
            <div style={style}>
                {this.state.topics.map(topic => (
                    <MentorTopicLink
                        key={topic.id.toString()}
                        title={topic.title}
                        description={topic.description}
                        isActive={topic.id == this.state.isActive ? true : false}
                        change={this.change}
                        id={topic.id}
                        mentors={topic.mentors}
                        curriculumId={topic.curriculum} />
                ))}
            </div>
        );
    }
}
