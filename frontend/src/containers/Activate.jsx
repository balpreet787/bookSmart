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
            <button className='mt-28 rounded-xl mx-auto bg-blue-500 px-8 py-2 text-white' onClick={activate_account}>Activate Account</button>
        </div>
    );
}


export default connect(null, { activate })(Activate);
