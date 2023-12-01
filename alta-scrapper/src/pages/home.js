import React, { useState} from "react";
import { useNavigate  } from 'react-router-dom';
import { Button, Label, TextInput } from 'flowbite-react';
import { useRedirectFunctions, useAuthInfo} from "@propelauth/react";

export default function Home() {
    let user
    const [web_id_helper_text, set_web_id_helper_text] = useState(<></>)
    let navigate = useNavigate();

    function RetrieveUser() {
        const authInfo = useAuthInfo();
        if (authInfo.loading) {
            return <div>Loading...</div>;
        } else if (authInfo.isLoggedIn) {
            user = authInfo.user
        } else {
            navigate('/welcome');
        }
    }

    async function saveWebId(e) {
        e.preventDefault()
        const requestOptions = {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(
                {
                    web_id: e.target.webId.value,
                    userId: user.userId
                })
        };
        const response = await fetch('/api/saveWebId', requestOptions);
        let data = await response.json();
        set_web_id_helper_text(<></>)
        if (data.response === "Web ID Already Used") {
            set_web_id_helper_text(<>
                <span className="font-medium">Oops!</span> That Web ID is already being used!
              </>)
        }
    }


    return (
        <div>
            {RetrieveUser()}
            <form className="flex max-w-md flex-col gap-4" onSubmit={saveWebId}>
                <div>
                    <div className="mb-2 block">
                        <Label htmlFor="webId" value="Enter Your Web ID found on your Alta Season Pass" />
                    </div>
                    <TextInput id="webId" placeholder="XXXXXXXX-XXX-XXX" required helperText={web_id_helper_text}/>
                </div>
                <Button type="submit">Submit</Button>
            </form>
        </div>
    )
}
