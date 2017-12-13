import React from 'react';
import {getLiterature} from './ItemService.js';

const style = {
    fontSize: 24,
    paddingTop: 16,
    marginBottom: 12,
    fontWeight: 400,
    height: 270,
};

class Literature extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return( 
            <div style={style} >
                <h2>Literature</h2>
                <ul>
                    {this.props.list.map((item) => (
                        <li key={item.toString()}>
                            {item}
                        </li>
                    ))}
                </ul>
            </div>
        );
    }
}

export default Literature;
