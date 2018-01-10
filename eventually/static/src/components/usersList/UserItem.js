import React from 'react';
import {Card, CardHeader} from 'material-ui/Card';
import Avatar from 'material-ui/Avatar';
import RaisedButton from 'material-ui/RaisedButton';
import {lightGreen400} from 'material-ui/styles/colors';

const cardHeaderStyle = {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer'
};

const titleStyle = {
    fontWeight: 'bold',
    fontSize: '18px'
};

const contentWrapperStyle = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center'
};

const buttonStyle = {
    marginRight: 10
};

export default class UserItem extends React.Component {

    constructor(props) {
        super(props);
    }

    handleClick = this.props.onButtonClick;

    render() {
        return (
            <div>
                <Card>
                    <div style={contentWrapperStyle}>
                        <CardHeader
                            style={cardHeaderStyle}
                            title={`${this.props.firstName} ${this.props.lastName}`}
                            avatar={<Avatar src={`https://robohash.org/${this.props.avatar}`}/>}
                            titleStyle={titleStyle}
                            onClick={this.handleClick}
                        />
                        <RaisedButton
                            label="Assign"
                            backgroundColor={lightGreen400}
                            style={buttonStyle}
                            onClick={this.handleClick}
                        />
                    </div>
                </Card>
            </div>
        );
    }
}