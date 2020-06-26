import React from 'react';
import moment from 'moment';
// import 'react-dates/initialize';
// import 'react-dates/lib/css/_datepicker.css';
// import { SingleDatePicker } from 'react-dates';

export default class CaseForm extends React.Component {
    constructor(props) {
        super (props);

        this.state ={
            mimnumber: props.casee? props.casee.mimnumber:' ',
            events: props.casee? props.casee.events:' ',
            createAt: props.casee? moment(props.casee.createAt): moment(),
            focused: false,
            error: ''  
        };
    }

    onMimNumChange = (e) =>{
        const mimnumber = e.target.value;
        if ( !mimnumber || mimnumber.match(/^[Mm][Ii][Mm]\d+$/)){
            this.setState( ()=> ({mimnumber}))
        }
    }
    onEventsChange = (e) => {
        const eventss = e.target.value;
        const events = eventss.split('\r');

        this.setState( () => ({events}))
    }
    onDateChange = (createAt) => {
        if (createAt) {
            this.setState( () => ({createAt}));
        }
    }
    onFocusChange = ({focused}) => {
        this.setState( () => ({ focused }));
    }
    onSubmit = (e) => {
        e.preventDefault();

        if ( !this.state.mimnumber || !this.state.events ) {
            this.setState( () => ( {error: 'submitted with nothing'}));
        }
        else{
            this.setState( () => ( {error:''}));
            console.log('submit');
            this.props.onSubmit({
                mimnumber: this.state.mimnumber,
                events: this.state.events,
                createAt: this.state.createAt.valueOf()
            })
        }

    }

    render() {
        return (
            <div>
                {this.state.error && <p>{this.state.error}</p>}
                <form onSubmit={this.onSubmit}>
                    <input
                        type="text"
                        placeholder="Mim-Number"
                        autoFocus
                        value={this.state.mimnumber}
                        onChange={this.onMimNumChange}
                    />
                    <textarea
                        placeholder="Add Your Event"
                        value={this.state.events}
                        onChange={this.onEventsChange}
                    />
                    {/* <SingleDatePicker
                        date={this.state.createAt}
                        onDateChange={this.onDateChange}
                        focused={this.state.focused}
                        onFocusChange={this.onFocusChange}
                        numberOfMonths={1}
                        isOutsideRange={ () => false }
                    /> */}
                </form>
            </div>
        )
    }
 

}