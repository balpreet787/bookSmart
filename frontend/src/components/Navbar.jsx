import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import setting from '../assets/setting.svg';


const Navbar = ({ isAuthenticated }) => {

    const authLinks = (
        <div className="space-x-4">
            <Link to="/settings"><img src={setting} className=" h-14 w-10" alt="Settings" /></Link>
        </div>
    );



    return (
        <nav className="flex items-center justify-between px-4 py-1 bg-blue-500">
            <div className="text-white">
                <h1 className="text-2xl font-bold"> <Link to="/">BookSmart</Link>
                </h1>
            </div>
            <div>
                {isAuthenticated ? authLinks : null}
            </div>
        </nav>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated
});

export default connect(mapStateToProps, {})(Navbar);
