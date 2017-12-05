import React from 'react';

export default class ProgressGraph extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={this.props.style}>
                <img style={{'width': '100%'}} src="https://datavizcatalogue.com/methods/images/top_images/area_graph.png" alt=""/>
            </div>
        );
    }
}
