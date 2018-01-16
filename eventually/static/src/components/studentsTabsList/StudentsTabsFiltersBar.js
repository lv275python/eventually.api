import React from 'react';
import Toggle from 'material-ui/Toggle';
import Paper from 'material-ui/Paper';
import SelectField from 'material-ui/SelectField';
import MenuItem from 'material-ui/MenuItem';
import DatePicker from 'material-ui/DatePicker';

const studentsTabsFiltersBarStyles = {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px 20px',
    margin: '1px'
};

const topicsSelectFieldStyles = {
    width: 200
};

const datePickerStyles = {
    width: 150
};

const isDoneToggleStyles = {
    width: 100
};

export default class StudentsTabsFiltersBar extends React.Component {

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <div style={this.props.style}>
                <Paper zDepth={1} >
                    <div style={studentsTabsFiltersBarStyles}>
                        <SelectField
                            floatingLabelText='Topic'
                            floatingLabelFixed={true}
                            value={this.props.topicValue}
                            onChange={this.props.onFiltersTopicsChange}
                            style={topicsSelectFieldStyles}
                        >
                            <MenuItem value={1} primaryText='Python' />
                            <MenuItem value={2} primaryText='JavaScript' />
                            <MenuItem value={5} primaryText='Swift' />
                        </SelectField>
                        <DatePicker 
                            floatingLabelText='From'
                            textFieldStyle={datePickerStyles}
                            value={this.props.fromDate}
                            onChange={this.props.onFiltersFromDateChange}
                        />
                        <DatePicker
                            floatingLabelText='To'
                            textFieldStyle={datePickerStyles}
                            value={this.props.toDate}
                            onChange={this.props.onFiltersToDateChange}
                        />
                        <Toggle
                            label='Is done' 
                            labelPosition='right' 
                            style={isDoneToggleStyles}
                            onToggle={this.props.onFiltersIsDoneToggle}
                        />
                    </div>
                </Paper>
            </div>
        );
    }
}
