import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuthInfo } from "@propelauth/react";
import { Spinner } from 'flowbite-react';
import NavBar from "../components/NavBar";
import FooterCustom from "../components/FooterCustom";
import SeasonTotalCard from "../components/SeasonTotalCard";
import LastDayCard from "../components/LastDayCard";
import ChairliftCard from "../components/ChairliftCard";
import DayTable from "../components/DayTable";

export default function Home() {
    let user
    let bearerToken
    const [user_snow_data, set_user_snow_data] = useState()
    const [last_day_skied_data, set_last_day_skied_data] = useState()
    const [ski_data, set_ski_data] = useState()
    let navigate = useNavigate();
    RetrieveUser()

    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            bearerToken = `Bearer ${authInfo.accessToken}`
            user = authInfo.user
            if (!user_snow_data) {
                getUserSnowData(user.userId)
            }
        } else {
            navigate('/welcome');
        }
    }

    async function getUserSnowData(userId) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json', "Authorization": bearerToken },
        };
        const response = await fetch(`/api/getUserSnowData/${userId}`, requestOptions);
        let data = await response.json();
        if (data.web_id == null) {
            navigate('/web_id')
        }
        else if (data.userName == null) {
            navigate('/set_username')
        }
        else {
            set_user_snow_data(data)
        }
        if (!last_day_skied_data && data.web_id) {
            getLastDaySkied(user.userId)
        }
        if (!ski_data && data.web_id) {
            getSkiDays(user.userId)
        }
        return
    }

    async function getLastDaySkied(userId) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json', "Authorization": bearerToken },
        };
        const response = await fetch(`/api/lastDay/${userId}`, requestOptions);
        let data = await response.json();
        if (data.dailyDataId != null) {
            set_last_day_skied_data(data)
        }
        return
    }

    async function getSkiDays(userId) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json', "Authorization": bearerToken },
        };
        const response = await fetch(`/api/skiData/${userId}`, requestOptions);
        let data = await response.json();
        if (data[0].dailyDataId != null) {
            set_ski_data(data)
        }
        return
    }

    return (
        <div className="App">
            <NavBar />
            <div>
                <div>
                    {user_snow_data && last_day_skied_data && ski_data ? <div>
                        <h3 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-3xl lg:text-6xl dark:text-white">Hey, {user_snow_data.userName}</h3>
                        <div className="flex flex-row">
                            <div className="w-1/2 flex-1">
                                <DayTable dayData={ski_data} />
                            </div>

                            <div className="w-1/2 flex-1 flex-wrap justify-around">
                                <SeasonTotalCard user_snow_data={user_snow_data} />

                            </div>
                        </div>
                            <div className="flex-1 flex-row">
                                <div className="w-1/2 flex-1 flex-wrap justify-around">

                                    <LastDayCard last_day_skied_data={last_day_skied_data} />


                                <div className="w-1/2 flex flex-wrap justify-around ">


                                    <ChairliftCard user_snow_data={user_snow_data} />
                                </div>
                            </div>
                        
                    </div> : <Spinner aria-label="Default status example" className="h-screen items-center" />}

                </div>

            </div >
            <FooterCustom />

        </div >
    )
}
