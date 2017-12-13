import React from 'react';
import Divider from 'material-ui/Divider';
import Paper from 'material-ui/Paper';
import ItemUnit from './ItemUnit';
import ItemsListTitle from './ItemsListTitle';

const titleText = 'Assignments for execute:';

export default class ItemsList extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={this.props.style}>
                <ItemsListTitle text={titleText} />
                <Paper zDepth={2}>
                    {
                        this.props.items.map(item => (
                            <ItemUnit key={item.id.toString()}
                                name={item.name}
                                description={item.description}
                                form={item.form}
                            />)
                        )
                    }
                    <Divider inset={true} />
                </Paper>
            </div>
        );
    }
}
