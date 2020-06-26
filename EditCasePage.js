import React from 'react';
import CaseForm from './CaseForm';
import { connect } from 'react-redux';
import { editCase,removeCase} from '../actions/mimCases';

const EditCasePage = (props) => {
    console.log(props);
    return (
        <div>
            from edit page
            <CaseForm
                casee = {props.casee}
                onSubmit = { (casee) => {
                    console.log('update', casee);
                    props.dispatch(editCase(props.casee.id, casee));
                    props.history.push('/mim-man');
                }}
            />
            <button onClick={ () => {
                props.dispatch(removeCase({id: props.casee.id}));
                props.history.push('/mim-man');
            }}>Remove</button>
        </div>
    )
}

const mapStateToProps = (state, props) => {
    return {
        casee: state.cases.find( (casee) => {
            return casee.id === props.match.params.id;
        })
    }
}

export default connect(mapStateToProps)(EditCasePage);