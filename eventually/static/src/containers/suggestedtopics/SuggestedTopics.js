import React from 'react';
import {getSuggestedTopicsService, putSuggestedTopicsItem} from './SuggestedTopicsService';
import SuggestedTopicsItem from './SuggestedTopicsItem';
import SuggestedTopicCreate from './SuggestedTopicCreate';
import {getUserId} from 'src/helper';
import {getProfileService} from 'src/containers';

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

    updateSuggestedTopicsItem = (id, name, description, interestedUser) => {
        const suggestedTopics = this.state.suggestedTopics;
        suggestedTopics.forEach(topic => {
            if(topic.id == id){
               topic.name = name;
               topic.description = description;
               getProfileService(interestedUser).then(response => {
                   let newUser = topic.interested_users_name;
                   newUser.push(response.data['first_name']);
                   this.setState(newUser);
               })
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
                        interestedUsersId = {suggestedTopics.interested_users}
                        interestedUsersName = {suggestedTopics.interested_users_name}
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