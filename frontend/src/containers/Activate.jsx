import React, { useState } from 'react';
import { Navigate, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { activate } from '../actions/auth';

const Activate = ({ activate }) => {
    const [userActivated, setUserActivated] = useState(false);
    const { uid, token } = useParams();

    const activate_account = () => {

        activate(uid, token);
        setUserActivated(true);
    }
    if (userActivated) {
        return <Navigate to='/login' />;
    }

    return (
        <div>
            <h1>Activate Account</h1>
            <button className='btn btn-primary mt-3' onClick={activate_account}>Activate Account</button>
        </div>
    );
}


export default connect(null, { activate })(Activate);
