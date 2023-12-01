import React, { useState, useEffect } from "react";
import './App.css';
import {
  useRedirectFunctions,
  useAuthInfo
} from "@propelauth/react";

function SignupAndLoginButtons() {
  const { redirectToSignupPage, redirectToLoginPage } = useRedirectFunctions();
  return (
    <div>
      <button onClick={redirectToSignupPage}>Signup</button>
      <button onClick={redirectToLoginPage}>Login</button>
    </div>
  );
}

function MinimalExample() {
  const authInfo = useAuthInfo();

  // Unlike the higher order functions, we need to check the loading case now
  if (authInfo.loading) {
    return <div>Loading...</div>;
  } else if (authInfo.isLoggedIn) {
    createUser(authInfo.user)
  } else {
    return <div>You are not logged in</div>;
  }
}

async function createUser(user) {
  const requestOptions = {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: user.email })
  };
  const response = await fetch('/createUser', requestOptions);
  const data = await response.json();
  console.log(data)
}


function App() {

  return (
    <div className="App">
      {SignupAndLoginButtons()}
      {MinimalExample()}
    </div>
  );
}

export default App;
