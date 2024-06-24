import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { signup } from '../actions/auth';

const SignUp = ({ signup, isAuthenticated }) => {
    const [accountCreated, setAccountCreated] = useState(false);
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: '',
        re_password: '',
    });

    const { name, email, password, re_password } = formData;

    const onChange = e =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        if (password === re_password) {
            signup(name, email, password, re_password);
            setAccountCreated(true);
        }
    }

    if (isAuthenticated) {
        return <Navigate to='/' />;
    }
    if (accountCreated) {
        return <Navigate to='/login' />;
    }

    return (
        <div>
            <h1 className='text-2xl mt-10 text-center'>Sign Up</h1>
            <form className='mx-auto flex flex-col gap-3 w-3/4' onSubmit={e => onSubmit(e)}>
                <div>
                    <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                        type='text'
                        placeholder='Name'
                        name='name'
                        value={name}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div>
                    <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                        type='email'
                        placeholder='Email*'
                        name='email'
                        value={email}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div>
                    <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                        type='password'
                        placeholder='Password*'
                        name='password'
                        value={password}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <div>
                    <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                        type='password'
                        placeholder='Confirm Password*'
                        name='re_password'
                        value={re_password}
                        onChange={e => onChange(e)}
                        required
                    />
                </div>
                <button className='mt-5 rounded-xl mx-auto bg-blue-500 px-8 py-2 text-white' type='submit'>Sign Up</button>
            </form>
            <p className='mt-10 mx-auto flex justify-center gap-4'>
                Already have an account? <Link to='/login'><span className='text-blue-500 border p-2 rounded-xl'>Login</span></Link>
            </p>
        </div>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
}); // mapStateToProps

export default connect(mapStateToProps, { signup })(SignUp);
