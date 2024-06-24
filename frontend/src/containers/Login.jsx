import React, { useState } from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';
import { login } from '../actions/auth';
import logo from '../assets/logo.svg';

const Login = ({ login, isAuthenticated }) => {
    console.log('Login isAuthenticated:', isAuthenticated);
    const [formData, setFormData] = useState({
        email: '',
        password: '',
    });

    const { email, password } = formData;

    const onChange = e =>
        setFormData({ ...formData, [e.target.name]: e.target.value });

    const onSubmit = async e => {
        e.preventDefault();
        await login(email, password);
    }

    if (isAuthenticated) {
        return <Navigate to='/' />;
    }

    return (
        <div >
            <img className='mx-auto' src={logo} alt='logo' />
            <div className='flex flex-col justify-center mt-6 gap-10'>
                <form className='mx-auto flex flex-col gap-3 w-3/4' onSubmit={e => onSubmit(e)}>
                    <div>
                        <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                            type='email'
                            placeholder='Email'
                            name='email'
                            value={email}
                            onChange={e => onChange(e)}
                            required
                        />
                    </div>
                    <div>
                        <input className='border-b p-2 w-full focus:outline-none focus:border-black'
                            type='password'
                            placeholder='Password'
                            name='password'
                            value={password}
                            onChange={e => onChange(e)}
                            required
                        />
                    </div>
                    <button className='mt-5 rounded-xl mx-auto bg-blue-500 px-8 py-2 text-white' type='submit'>Login</button>
                </form>
                <div className='mx-auto flex flex-col gap-4'>
                    <p className='mt-3'>
                        Don&apos;t have an account? <Link to='/signup'><span className='text-blue-500 border p-2 rounded-xl'>Sign Up</span></Link>
                    </p>
                    <p className='mt-3'>
                        Forgot your password? <Link to='/reset-password'><span className='text-blue-500 border p-2 rounded-xl'>Reset Password</span></Link>
                    </p>
                </div>
            </div>
        </div>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
}); // mapStateToProps

export default connect(mapStateToProps, { login })(Login);
