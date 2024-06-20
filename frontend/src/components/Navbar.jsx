import React from 'react';
import { Link } from 'react-router-dom';
import { logout } from '../actions/auth';
import { connect } from 'react-redux';


const Navbar = ({ logout, isAuthenticated }) => {
    const guestLinks = (
        <div className="space-x-4">
            <Link to="/login" className="px-4 py-2 text-white bg-blue-700 rounded-md">Login</Link>
            <Link to="/signup" className="px-4 py-2 text-white bg-blue-700 rounded-md">Sign Up</Link>
        </div>
    );

    const authLinks = (
        <div className="space-x-4">
            <Link to="/settings" className="px-4 py-2 text-white bg-blue-700 rounded-md">Settings</Link>
            <a href='#!' onClick={logout} className="px-4 py-2 text-white bg-blue-700 rounded-md">Logout</a>
        </div>
    );



    return (
        <nav className="flex items-center justify-between p-4 bg-blue-500">
            <div className="text-white">
                <h1 className="text-2xl font-bold">BookSmart</h1>
            </div>
            <div>
                {isAuthenticated ? authLinks : guestLinks}
            </div>
        </nav>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, { logout })(Navbar);
