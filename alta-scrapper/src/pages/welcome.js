import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { Button } from 'flowbite-react';
import {
    useRedirectFunctions,
    useAuthInfo
} from "@propelauth/react";




function App() {
    const { redirectToSignupPage, redirectToLoginPage } = useRedirectFunctions()
    let navigate = useNavigate();
    RetrieveUser()
    
    

    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            loginUser(authInfo.user)
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
            <div classNameName="flex items-center justify-center">

                <section className="bg-white dark:bg-gray-900">
                    <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16">
                        <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">AltaTracker</h1>
                        <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-48 dark:text-gray-400">Welcome to your personal skiing companion at Alta Ski Area! Our app allows you to track your days, lifts, and elevation skied, providing you with detailed insights into your skiing data. Compete with others to see who has the most days skied, or simply enjoy a comprehensive overview of your own skiing journey. With AltaTracker, every day on the slopes is a day to remember. Start your adventure with us today!</p>
                        <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                        <Button onClick={redirectToSignupPage}>SignUp</Button>
                        <Button onClick={redirectToLoginPage} color="blue">Login</Button>
                            <a href="https://github.com/pfvatterott/alta-web-scrape" className="inline-flex justify-center items-center py-3 px-5 text-base font-medium text-center text-gray-900 rounded-lg border border-gray-300 hover:bg-gray-100 focus:ring-4 focus:ring-gray-100 dark:text-white dark:border-gray-700 dark:hover:bg-gray-700 dark:focus:ring-gray-800">
                                Learn more
                            </a>
                        </div>
                    </div>
                </section>

            </div>
        </div>
    );
}

export default App;
