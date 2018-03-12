import React from 'react';
import {ItemLink, getItemListService} from 'src/containers';


export default class TopicItemList extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isActive: -1,
            isModalOpen: false,
            answer: '',
            items:[]
        };
    }

    componentWillMount() {
        getItemListService(this.props.curriculumId, this.props.topicId).then(response => {
            this.setState({items: response.data['items']});
        });
    }


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

    handleClick = id => {
        if (this.state.isActive === id) {
            this.setState({isActive: -1});
        } else {
            this.setState({isActive: id});
        }
    };

    render() {
        return (
            <div style={this.props.style}>
                {this.state.items.map(item => (
                    <ItemLink
                        key={item.id.toString()}
                        name={item.name}
                        description={item.description}
                        form={item.form}
                        isActive={item.id === this.state.isActive || false}
                        onClick={this.handleClick}
                        id={item.id}
                        onModalOpen={this.handleModalOpen}
                    />)
                )}
            </div>
        );
    }
}
