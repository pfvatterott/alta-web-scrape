import React, { useState } from "react";
import { useNavigate } from 'react-router-dom';
import { useAuthInfo } from "@propelauth/react";
import { Spinner } from 'flowbite-react';
import NavBar from "../components/NavBar";
import FooterCustom from "../components/FooterCustom";
import SeasonTotalCard from "../components/SeasonTotalCard";
import LastDayCard from "../components/LastDayCard";

export default function Home() {
    let user
    const [user_snow_data, set_user_snow_data] = useState()
    const [last_day_skied_data, set_last_day_skied_data] = useState()
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

    async function getUserSnowData(userId) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
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
        return
    }

    async function getLastDaySkied(userId) {
        const requestOptions = {
            method: 'GET',
            headers: { 'Accept': 'application/json' },
        };
        const response = await fetch(`/api/lastDay/${userId}`, requestOptions);
        let data = await response.json();
        if (data.dailyDataId != null) {
            set_last_day_skied_data(data)
        }
        return
    }

    return (
        <div className="App">
            <NavBar />
            <div classNameName="flex">
                <section className="bg-white dark:bg-gray-900">

                    {user_snow_data && last_day_skied_data ? <div>
                        <h3 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-3xl lg:text-6xl dark:text-white">Hey, {user_snow_data.userName}</h3>
                        <div className="py-8 px-4 mx-auto max-w-screen-xl lg:py-16">
                            <SeasonTotalCard user_snow_data={user_snow_data} />
                            <LastDayCard last_day_skied_data={last_day_skied_data} />
                        </div>
                    </div> : <Spinner aria-label="Default status example" className="h-screen items-center"/>}

                </section>

            </div >
            <FooterCustom />

        </div >
    )
}
