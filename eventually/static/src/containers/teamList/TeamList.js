import React from 'react';
import TeamItem from './TeamItem';
import {teamServiceGet} from './teamService';

export default class TeamList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            teams:[],
        };
    }

    componentWillMount(){
        this.getTeamItem();
    }

    getTeamItem = () => {
        teamServiceGet().then(response => this.setState({'teams': response.data.teams}));
    };

    updateTeamItem = (id, name, description, image) => {
        const teams = this.state.teams;
        teams.forEach(team => {
            if(team.id == id){
                team.name = name;
                team.description = description;
                team.image = image;
            }
        });
        this.setState({'teams': teams});
    };

    render() {
        return (
            <div>
                {this.state.teams.map(team => (
                    <TeamItem
                        key={team.id.toString()}
                        id={team.id}
                        name={team.name}
                        description={team.description}
                        image={team.image}
                        members={team.members_id.length}
                        updateItem={this.updateTeamItem}
                        listOfMembers={team.members_id}
                    />
                ))}
            </div>
        );
    }
}
