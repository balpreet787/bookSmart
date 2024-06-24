import React from "react";
import { Link, Navigate } from "react-router-dom";
import { connect } from "react-redux";
import { logout } from "../actions/auth";

const Navbar = ({ logout, isAuthenticated }) => {

    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }

    return (
        <div className="flex flex-col p-3 text-center">
            <span className="border-b py-4">
                <Link to="/change-username">Edit Name</Link>
            </span>
            <span className="border-b py-4">
                <Link to="/reset-password">Reset Password</Link>
            </span>
            <span className="border-b py-4">
                <Link to="/login" onClick={logout}>Logout</Link>
            </span>
        </div>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps, { logout })(Navbar);