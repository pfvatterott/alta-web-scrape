import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import {AuthProvider} from "@propelauth/react";


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AuthProvider 
    authUrl={"https://262233167.propelauthtest.com"} 
    >
    <App />
  </AuthProvider>
);

