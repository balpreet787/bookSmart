import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Layout from "./hocs/Layout";
import Home from "./containers/Home";
import Login from "./containers/Login";
import SignUp from "./containers/Signup";
import Activate from "./containers/Activate";
import ResetPassword from "./containers/ResetPassword";
import ResetPasswordConfirm from "./containers/ResetPasswordConfirm";
import Settings from "./containers/Settings";
import { Provider } from 'react-redux';
import store from "./store";

const App = () => (
  <Provider store={store}>
    <Router>
      <div className="">
        <Layout>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/signup" element={<SignUp />} />
            <Route path="/activate/:uid/:token" element={<Activate />} />
            <Route path="/reset-password" element={<ResetPassword />} />
            <Route path='settings' element={<Settings />} />
            <Route path="/password/reset/confirm/:uid/:token" element={<ResetPasswordConfirm />} />
          </Routes>
        </Layout>
      </div>
    </Router>
  </Provider>
);

export default App;
