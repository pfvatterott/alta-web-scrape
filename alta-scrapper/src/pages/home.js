import React, { useState} from "react";
import { useNavigate  } from 'react-router-dom';
import { Button, Label, TextInput } from 'flowbite-react';
import { useAuthInfo} from "@propelauth/react";

export default function Home() {
    let user
    const [web_id_helper_text, set_web_id_helper_text] = useState(<></>)
    const [user_snow_data, set_user_snow_data] = useState(<></>)
    let navigate = useNavigate();
    RetrieveUser()

    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            user = authInfo.user
            if (!user_snow_data) {
                getUserSnowData(user.userId)
            }
        } else {
            navigate('/welcome');
        }
    }

    async function getUserSnowData(userId){
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
        };
        const response = await fetch(`/api/getUserSnowData/${userId}`, requestOptions);
        let data = await response.json();
        if (data.web_id == null) {
            navigate('/web_id')
        }
        else {
            set_user_snow_data(data)
        }
    }

    return (
        <div>
            <h1>Hey</h1>
        </div>
    )
}
