import expect from 'expect';
import React from 'react';
import sinon from 'sinon';
import {shallow, configure, render, mount} from 'enzyme';
import Adapter from 'enzyme-adapter-react-16';
import EventEdit from '../../event/EventEdit';
import * as EventService from '../../event/EventService';


configure({ adapter: new Adapter() });

describe('Component EventEdit Tests', () => {
    const renderComponent = (props) => {
        const defaultProps = {
            id: 1,
            teams: [1,2,3],
            open: false,
            teamId: 1,
            owner: 1,
            name: 'Old Name',
            description: 'Old Description',
            startAt: 1509539867,
            duration: 124234,
            budget: 1000,
            status: 0
        };
        const componentProps = Object.assign({},defaultProps, props);
        return shallow(<EventEdit {...componentProps}/>);
    };

    describe('Basic Tests', ()=> {
        it('renders if EventEdit Component exists', () => {
            const wrapper = renderComponent();
            expect(wrapper.exists()).toEqual(true);
        });

        it('check if render TextField, DatePicker, TimePicker, SelectField exists', () => {
            const wrapper = renderComponent();
            expect(wrapper.find('TextField').exists()).toEqual(true);
            expect(wrapper.find('SelectField').exists()).toEqual(true);
            expect(wrapper.find('DatePicker').exists()).toEqual(true);
            expect(wrapper.find('TimePicker').exists()).toEqual(true);

        });

        it('check the quantity of TextField', () => {
            const wrapper = renderComponent();
            expect(wrapper.find('TextField').length).toEqual(3);
        });

        it('check the quantity of SelectField', () => {
            const wrapper = renderComponent();
            expect(wrapper.find('SelectField').length).toEqual(2);
        });

        it('check the quantity of DatePicker', () => {
            const wrapper = renderComponent();
            expect(wrapper.find('DatePicker').length).toEqual(2);
        });

        it('check the quantity of TimePicker', () => {
            const wrapper = renderComponent();
            expect(wrapper.find('TimePicker').length).toEqual(2);
        });
    });

    describe ('Change the state tests', () =>{
        it('check input change on state name', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().name).toEqual('Old Name');
            wrapper.find('#name-input').simulate('Change',{ target: { value: 'New Name'}});
            expect(wrapper.state().name).toBe('New Name');
        });

        it('check input change on state description', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().description).toEqual('Old Description');
            wrapper.find('#description-input').simulate('Change',{ target: { value: 'New Description'}});
            expect(wrapper.state().description).toBe('New Description');
        });

        it('check input change on state budget', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().budget).toEqual(1000);
            wrapper.find('#budget-input').simulate('Change',{ target: { value: '3000'}});
            expect(wrapper.state().budget).toBe(3000);
        });

        it('check input state budget null', () => {
            const wrapper = renderComponent({budget:null});
            expect(wrapper.state().budget).toEqual(0);
        });

        it('check input change on state date', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().startAt).toEqual(1509539867);
            const event = sinon.spy;
            wrapper.find('#start-date-input').simulate('Change', event, 1514764800000);
            expect(wrapper.state().startAt).toEqual(1514764800);
        });

        it('check input change on state status', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().status).toEqual(0);
            const event = sinon.spy;
            wrapper.find('#status-input').simulate('Change', event,2,2);
            expect(wrapper.state().status).toEqual(2);
        });
    });

    describe ('Check if handleFunctions called', () =>{

        it('check if handleName called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleName');
            wrapper.find('#name-input').simulate('Change',{ target: { value: 'Very New Name'}});
            wrapper.update();
            wrapper.find('#name-input').simulate('Change',{ target: { value: 'Very New Name'}});
            expect(spy.called).toEqual(true);
        });

        it('check if handleDescription called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleDescription');
            wrapper.find('#description-input').simulate('Change',{ target: { value: 'Very New Description'}});
            wrapper.update();
            wrapper.find('#description-input').simulate('Change',{ target: { value: 'Very New Description'}});
            expect(spy.called).toEqual(true);
        });

        it('check if handleStartAt called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleStartAt');
            wrapper.find('#start-date-input').simulate('Change');
            wrapper.update();
            wrapper.find('#start-date-input').simulate('Change');
            expect(spy.called).toEqual(true);
        });

        it('check if handleDuration called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleDuration');
            wrapper.find('#end-date-input').simulate('Change');
            wrapper.update();
            wrapper.find('#end-date-input').simulate('Change');
            expect(spy.called).toEqual(true);
        });

        it('check if handleTeams called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleTeams');
            wrapper.find('#teams-input').simulate('Change');
            wrapper.update();
            wrapper.find('#teams-input').simulate('Change');
            expect(spy.called).toEqual(true);
        });

        it('check if handleBudget called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleBudget');
            wrapper.find('#budget-input').simulate('Change',{ target: { value: 2000}});
            wrapper.update();
            wrapper.find('#budget-input').simulate('Change',{ target: { value: 2000}});
            expect(spy.called).toEqual(true);
            expect(wrapper.state().budget).toEqual(2000);
        });

        it('check if handleStatus called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleStatus');
            wrapper.find('#status-input').simulate('Change');
            wrapper.update();
            wrapper.find('#status-input').simulate('Change');
            expect(spy.called).toEqual(true);
        });

        it('check if handleSave called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleSave');
            wrapper.instance().handleSave();
            expect(spy.called).toEqual(true);
        });

        it('check if handleOpen called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleOpen');
            wrapper.find('RaisedButton').simulate('Click');
            wrapper.update();
            wrapper.find('RaisedButton').simulate('Click');
            expect(spy.called).toEqual(true);
        });

        it('check if handleClose called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'handleClose');
            wrapper.find('Dialog').simulate('RequestClose');
            wrapper.update();
            wrapper.find('Dialog').simulate('RequestClose');
            expect(spy.called).toEqual(true);
        });

        it('check if getTeamItem called', () => {
            const wrapper = renderComponent();
            const spy = sinon.spy(wrapper.instance(), 'getTeamItem');
            wrapper.instance().componentWillMount();
            expect(spy.called).toEqual(true);
        });

        it('check getTeamItem called and change the state', () => {
            const promise = Promise.resolve(
                {
                    data: {
                        teams: [
                            {'id':1, name: 'ProstoTeam'},
                            {'id':2, name: 'SuperTeam'}
                        ]
                    }
                });
            sinon.stub(EventService, 'GetTeamsListService').callsFake(() => promise);
            const wrapper = renderComponent();
            return promise
                .then(() => {
                    expect(wrapper.update().state().teams).toEqual(
                        [{'id': 1, 'name': 'ProstoTeam'}, {'id': 2, 'name': 'SuperTeam'}]
                    );
                });
        });
    });

    describe('Check Buttons click', () => {
        it('check if click on Edit Button changes state', () => {
            const wrapper = renderComponent();
            expect(wrapper.state().open).toEqual(false);
            wrapper.find('form').find('RaisedButton').simulate('Click');
            expect(wrapper.state().open).toEqual(true);
        });

        it('check if RequestClose changes state', () => {
            const wrapper = renderComponent({open:true});
            wrapper.find('form').find('RaisedButton').simulate('Click');
            expect(wrapper.state().open).toEqual(true);
            wrapper.find('form').find('Dialog').simulate('RequestClose');
            expect(wrapper.state().open).toEqual(false);
        });

    });

});
