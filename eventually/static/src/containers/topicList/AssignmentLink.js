import React from 'react';
import {List, ListItem} from 'material-ui/List';

const style = {
    border: '1px solid #616161',
    borderRadius: '5px',
    boxShadow: '5px 5px 10px #616161' 
}

export default class AssignmentItem extends React.Component {
    
        constructor(props) {
            super(props);
            this.state = {
                expanded: false,
            };
        }
render(){
    return(
            <div>
                <List>
                    <ListItem 
                        style = {style}
                        primaryText={this.props.title} />
                </List>
            </div>
        )
    }
}
