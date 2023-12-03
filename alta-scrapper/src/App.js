import React, { useState, useEffect } from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
} from "react-router-dom";
import './App.css';
import Welcome from "./pages/welcome"
import Home from "./pages/home"
import WebId from "./pages/webId";


function App() {
  return (
      <Router>
          <Routes>
              <Route exact path="/" element={<Welcome />} />
              <Route path="/home" element={<Home />} />
              <Route path="/web_id" element={<WebId />} />
          </Routes>
      </Router>
  );
}

export default App;
