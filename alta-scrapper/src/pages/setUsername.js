import React, { useState } from "react";
import { useAuthInfo } from "@propelauth/react";
import { useNavigate } from 'react-router-dom';
import { Button, Label, TextInput, Spinner } from 'flowbite-react';


export default function SetUsername() {
    let navigate = useNavigate();
    const [username_helper_text, set_username_helper_text] = useState(<></>)
    let user
    let bearerToken
    RetrieveUser()
  
    function RetrieveUser() {
      const authInfo = useAuthInfo();
      if (authInfo.loading) {
        return <div>Loading...</div>;
      } else if (authInfo.isLoggedIn) {
        bearerToken = `Bearer ${authInfo.accessToken}`
        user = authInfo.user
      } else {
        navigate('/welcome');
      }
    }
  
    async function saveUsername(e) {
      e.preventDefault()
      const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', "Authorization": bearerToken },
        body: JSON.stringify(
          {
            userName: e.target.username.value,
            userId: user.userId
          })
      };
      const response = await fetch('/api/saveUsername', requestOptions);
      let data = await response.json();
      if (data.response === "Username Already Used") {
        set_username_helper_text(<>
          <span className="font-medium">Oops!</span> That username is already being used!
        </>)
      }
      navigate('/home')
    }
  
    return (
      
      <div className="App">
        <div classNameName="flex items-center justify-center">
          <section className="bg-white dark:bg-gray-900">
            <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16">
              <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Create your username</h1>
              <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-48 dark:text-gray-400">This is how other members of AltaTracker will see you.</p>
              <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
                <form className="flex max-w-md flex-col gap-4" onSubmit={saveUsername}>
                  <div>
                    <div className="mb-2 block">
                      <Label htmlFor="username" value="Enter Your Username" />
                    </div>
                    <TextInput id="username" required helperText={username_helper_text} />
                  </div>
                  <Button type="submit">Submit</Button>
                </form>
              </div>
            </div>
          </section>
  
          
  
        </div>
  
      </div>
  
  
    )
  }
  
