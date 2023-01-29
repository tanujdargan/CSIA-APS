import React from "react";
import { Redirect } from "react-router-dom";

import { authStates, withAuth } from "../components/auth";
import { signOut } from "../utils/firebase";
import Loader from "../components/loader";

function handleSignOut() {
  signOut()
    .then(() => {
      console.log("Signed Out");
    })
    .catch(e => {
      console.log("Error signing out", e);
    });
}

class Home extends React.Component {
  render() {
    if (this.props.authState === authStates.INITIAL_VALUE) {
      return <Loader />;
    }

    if (this.props.authState === authStates.LOGGED_OUT) {
      return <Redirect to="/login"></Redirect>;
    }

    return <Redirect to="/logged-in-home.html"></Redirect>;
    }    
    }

export default withAuth(Home);
