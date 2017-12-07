import React from 'react';
import {List, ListItem} from 'material-ui/List';
import { Link } from 'react-router'
import {withRouter} from 'react-router-dom'


const style = {
    border: '1px solid #616161',
    borderRadius: '5px',
    boxShadow: '5px 5px 10px #616161' 
}

class AssignmentItem extends React.Component {
    
    constructor(props) {
        super(props);
        this.state = {
            expanded: false,
        };
    }
    handleId= () => {
        var link='/item/'+ this.props.id;
        this.props.history.push(link);
    }
    render(){
        return(
            <div>
                <List>
                    
                        <ListItem 
                            style = {style}
                            primaryText={this.props.title}
                            onClick={this.handleId} />
                </List>
            </div>
        )
    }
}

export default withRouter(AssignmentItem)