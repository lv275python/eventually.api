import React from 'react';
import { withRouter } from 'react-router-dom';
import Chip from 'material-ui/Chip';
import Avatar from 'material-ui/Avatar';


const chipStyle = {
    margin: 4,
};

class MentorsChip extends React.Component {

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
                    <Avatar src={this.props.photo} />
                    {this.props.text}
                </Chip>
            </div>
        );
    }
}

export default withRouter(MentorsChip);
