import React from 'react';
import TeamItem from './TeamItem';
import {teamServiceGet} from './teamService';
import CreateTeamDialog from './CreateTeamDialog';

const CreateTeamDialogStyle = {
    position: 'fixed',
    right: '3%',
    top: '85%'
};
const TeamListStyle = {
    marginBottom: '3%'
};

export default class TeamList extends React.Component {
    getTeamItem = () => {
        teamServiceGet(true).then(response => this.setState({'teams': response.data.teams}));
    };

    goToUserProfile = (id) => {
        this.props.history.push('/profile/' + id);
    };

    updateTeamItem = (id, name, description, image) => {
        const teams = this.state.teams;
        teams.forEach(team => {
            if (team.id == id) {
                team.name = name;
                team.description = description;
                team.image = image;
            }
        });
        this.setState({'teams': teams});
    };

    constructor(props) {
        super(props);
        this.state = {
            teams: [],
        };
    }

    componentWillMount() {
        this.getTeamItem();
    }

    render() {
        return (
            <div style={TeamListStyle}>
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
                        owner={team.owner_id}
                        goToUserProfile={this.props.goToUserProfile}
                    />
                ))}
                <CreateTeamDialog
                    style={CreateTeamDialogStyle}
                    getTeamItem={this.getTeamItem}
                />
            </div>
        );
    }
}
