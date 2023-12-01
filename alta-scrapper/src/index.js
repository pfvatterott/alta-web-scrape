import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import {RequiredAuthProvider, RedirectToLogin} from "@propelauth/react";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <RequiredAuthProvider 
    authUrl={"https://262233167.propelauthtest.com"} 
    displayIfLoggedOut={<RedirectToLogin />}
    >
    <App />
  </RequiredAuthProvider>
);

