import React from 'react';
import { reset_password } from '../actions/auth';
import { connect } from 'react-redux';
import { Navigate } from 'react-router-dom';

const ResetPassword = ({ reset_password }) => {
    const [requestSent, setRequestSent] = React.useState(false);
    const [formData, setFormData] = React.useState({
        email: '',
    });

    const { email } = formData;

    const onChange = e => setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        reset_password(email);
        setRequestSent(true);
    }
    if (requestSent) {
        return <Navigate to='/' />;
    }

    return (
        <div>
            <h1 className='text-2xl font-bold'>Reset Password</h1>
            <form className='form-group' onSubmit={e => onSubmit(e)}>
                <div>
                    <input className='border border-gray-300 rounded-md p-2'
                        type='email'
                        placeholder='Email'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <button className='bg-blue-500 text-white px-4 py-2 mt-3 rounded-md' type='submit'>Reset Password</button>
            </form>
        </div>
    );
}

export default connect(null, { reset_password })(ResetPassword);
