import React from 'react';
import { withRouter } from 'react-router-dom';
import Chip from 'material-ui/Chip';


const chipStyle = {
    margin: 4,
};

class InterestedUsersChips extends React.Component {

    constructor(props) {
        super(props);
    }
    handleClick = () => {
        this.props.history.push('/profile/' + this.props.id);
    };

    render() {
        return (
            <div>
                <Chip
                    onClick={this.handleClick}
                    style={chipStyle}>
                    {this.props.text}
                </Chip>
            </div>
        );
    }
}

export default withRouter(InterestedUsersChips);