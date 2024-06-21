import React from 'react';
import { Link, useParams } from 'react-router-dom';
import { connect } from 'react-redux';
import { reset_password_confirm } from '../actions/auth';
import { Navigate } from 'react-router-dom';

const ResetPasswordConfirm = ({ reset_password_confirm }) => {
    const [requestSent, setRequestSent] = React.useState(false);
    const [formData, setFormData] = React.useState({
        new_password: '',
        re_new_password: '',
    });

    const { new_password, re_new_password } = formData;
    const onChange = e =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const { uid, token } = useParams();

    const onSubmit = async e => {
        e.preventDefault();
        reset_password_confirm(uid, token, new_password, re_new_password);
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
                        type='password'
                        placeholder='New Password'
                        name='new_password'
                        value={new_password}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div>
                    <input className='border border-gray-300 rounded-md p-2'
                        type='password'
                        placeholder='Re-enter New Password'
                        name='re_new_password'
                        value={re_new_password}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <button className='bg-blue-500 text-white px-4 py-2 mt-3 rounded-md' type='submit'>Reset Password</button>
            </form>
        </div>
    );
}

export default connect(null, { reset_password_confirm })(ResetPasswordConfirm);
