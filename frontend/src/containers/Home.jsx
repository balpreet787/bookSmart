import React from 'react';
import { Link, Navigate } from 'react-router-dom';
import { connect } from 'react-redux';

const Home = ({ isAuthenticated }) => {

    if (!isAuthenticated) {
        return <Navigate to='/login' />;
    }
    return (
        <div>
            <h1>Home</h1>
            <p>Welcome to the Home page</p>
            <div>Lorem ipsum dolor sit amet consectetur adipisicing elit. Accusamus iusto repellendus explicabo vel consequuntur provident debitis ab qui possimus temporibus dignissimos, tenetur hic sapiente a? Itaque, reiciendis quidem suscipit, assumenda autem maxime at asperiores ad eius voluptates exercitationem rerum odit.</div>
            {/* login button */}
            <Link to='/login' className='btn btn-primary mt-3'>Login</Link>
        </div>
    );
}

const mapStateToProps = state => ({
    isAuthenticated: state.auth.isAuthenticated,
});

export default connect(mapStateToProps)(Home);
