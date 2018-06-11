import React from 'react';
import Divider from 'material-ui/Divider';
import Paper from 'material-ui/Paper';
import ItemUnit from './ItemUnit';
import getItemsList from './itemsListService';
import {SendAnswer} from 'src/components';

export default class ItemsList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isActive: -1,
            isModalOpen: false,
            answer: '',
            items: [],
        };
    }

    componentWillMount() {
        getItemsList(this.props.topicId, this.props.userId).then(response => {
            this.setState({items: response.data['assignments']});
        });
    };


    handleModalOpen = () => {
        this.setState({isModalOpen: true});
    };

    handleModalClose = () => {
        this.setState({isModalOpen: false});
    };

    handleAnswerChange = (event, value) => {
        this.setState({
            answer: value
        });
    };

    handleClick = (id) => {
        if (this.state.isActive === id) {
            this.setState({isActive: -1});
        } else {
            this.setState({isActive: id});
        }
    };

    render() {
        return (
            <div style={this.props.style}>
                <Paper zDepth={1}>
                    {this.state.items.map(item => (
                        <ItemUnit
                            key={item.item.id.toString()}
                            name={item.item.name}
                            description={item.item.description}
                            form={item.item.form}
                            isActive={item.item.id === this.state.isActive || false}
                            onClick={this.handleClick}
                            id={item.item.id}
                            assignment_id = {item.assignment.id}
                            onModalOpen={this.handleModalOpen}
                        />)
                    )
                    }
                    <Divider inset={true} />
                </Paper>
                <SendAnswer
                    answer={this.state.answer}
                    isModalOpen={this.state.isModalOpen}
                    onModalClose={this.handleModalClose}
                    onAnswerChange={this.handleAnswerChange}
                />
            </div>
        );
    }
}
