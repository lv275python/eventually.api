import React from 'react';
import Answer from './Answer.js';
import Assignment from './Assignment.js';
import Literature from './Literature.js';
import TimeLeft from './TimeLeft.js';
import {getData} from './ItemService.js';
import {Tabs, Tab} from 'material-ui/Tabs';

const styles = {
    headline: {
        fontSize: 24,
        paddingTop: 16,
        marginBottom: 12,
        fontWeight: 400,
    },
};

export default class Item extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            description: 'constructor',
            literatureList: [],
            timeToLive: 0,
        };
    }

    componentWillMount(){
        this.getItem();
    }

    getItem = () => {
        const data = getData(+this.props.match.params.itemId);
        this.setState({
            description: data.description,
            literatureList: data.literatureList,
            timeToLive: data.timeToLive});
    };

    render() {
        return (
            <div>
                <Tabs>
                    <Tab label='Assignment'>
                        <div style={styles.headline}>
                            <Assignment description={this.state.description}/>
                        </div>
                    </Tab>
                    <Tab label='Literature'>
                        <div style={styles.headline}>
                            <Literature list={this.state.literatureList}/>
                        </div>
                    </Tab>
                    <Tab label='Answer' >
                        <div style={styles.headline}>
                            <Answer/>
                        </div>
                    </Tab>
                </Tabs>
                <TimeLeft time={this.state.timeToLive}/>
            </div>
        );
    }
}
