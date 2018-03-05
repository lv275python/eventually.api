import React from 'react';
import {getSuggestedTopicsService, putSuggestedTopicsItem} from './SuggestedTopicsService';
import SuggestedTopicsItem from './SuggestedTopicsItem';
import SuggestedTopicCreate from './SuggestedTopicCreate';


const SuggestedTopicCreateStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};


export default class SuggestedTopics extends React.Component {
    constructor(props){
        super(props);
        this.state = {
            suggestedTopics:[]
        };
    }

    componentWillMount(){
        this.getSuggestedTopicsItem();
    }

    getSuggestedTopicsItem = () => {
        getSuggestedTopicsService().then(response => this.setState(
        {'suggestedTopics': response.data['suggested_topics']}));
    };

    updateSuggestedTopicsItem = (id, name, description) => {
        const suggestedTopics = this.state.suggestedTopics;
        suggestedTopics.forEach(topic => {
            if(topic.id == id){
               topic.name = name;
               topic.description = description;
            }
        });
        this.setState({'suggestedTopics': suggestedTopics});
    };


    render() {
        return(
            <div>
                {this.state.suggestedTopics.map(suggestedTopics => (
                    <SuggestedTopicsItem
                        key={suggestedTopics.id.toString()}
                        id={suggestedTopics.id}
                        name={suggestedTopics.name}
                        description={suggestedTopics.description}
                        owner = {suggestedTopics.owner}
                        interestedUsers = {suggestedTopics.interested_users}
                        updateTopic = {this.updateSuggestedTopicsItem}
                    />
                     ))}
                    <SuggestedTopicCreate
                    style={SuggestedTopicCreateStyle}
                    getSuggestedTopicsItem={this.getSuggestedTopicsItem}
                    />
            </div>
        )
    }
}