import React, { useState, useEffect } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuthInfo } from "@propelauth/react";
import { Spinner } from 'flowbite-react';
import NavBar from "../components/NavBar";
import FooterCustom from "../components/FooterCustom";

export default function LeaderBoard() {
    let bearerToken
    const [leader_data, set_user_data] = useState()
    let navigate = useNavigate();
    RetrieveUser()


    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            bearerToken = `Bearer ${authInfo.accessToken}`
            if (!leader_data) {
                getLeaders('vertical')
            }
        } else {
            navigate('/welcome');
        }
    }

    async function getLeaders(category) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json', "Authorization": bearerToken },
        };
        const response = await fetch(`/api/skiData/leaders/${category}`, requestOptions);
        let data = await response.json();
        console.log(data)
        set_user_data(data)
        return
    }

    
  return (
    <div>leaderBoard</div>
  )
}
