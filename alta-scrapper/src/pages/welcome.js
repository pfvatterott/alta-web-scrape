import React, { useState, useEffect } from "react";
import { useNavigate  } from 'react-router-dom';
import {
    useRedirectFunctions,
    useAuthInfo
} from "@propelauth/react";




function App() {
    let navigate = useNavigate();
    function SignupAndLoginButtons() {
        const { redirectToSignupPage, redirectToLoginPage } = useRedirectFunctions();
        return (
            <div>
                <button onClick={redirectToSignupPage}>Signup</button>
                <button onClick={redirectToLoginPage}>Login</button>
            </div>
        );
    }

    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            loginUser(authInfo.user)
        } else {
            return <div>You are not logged in</div>;
        }
    }

    async function loginUser(user) {
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    email: user.email,
                    userId: user.userId
                })
        };
        const response = await fetch('/api/login', requestOptions);
        await response.json();
        navigate('/home');
    }

    return (
        <div className="App">
            {SignupAndLoginButtons()}
            {RetrieveUser()}
        </div>
    );
}

export default App;
