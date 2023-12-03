import React, { useState } from "react";
import { useAuthInfo } from "@propelauth/react";
import { useNavigate } from 'react-router-dom';
import { Button, Label, TextInput, Spinner } from 'flowbite-react';

export default function WebId() {
  let navigate = useNavigate();
  const [web_id_helper_text, set_web_id_helper_text] = useState(<></>)
  const [is_loading, set_is_loading] = useState(false)
  let user
  RetrieveUser()

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
    set_is_loading(true)
    set_web_id_helper_text(<></>)
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
    if (data.response === "Web ID Already Used") {
      set_web_id_helper_text(<>
        <span className="font-medium">Oops!</span> That Web ID is already being used!
      </>)
    }
    else if (data.response === "Web ID Not Valid. Try Again") {
      set_web_id_helper_text(<>
        <span className="font-medium">Oops!</span> That Web ID is Not Valid. Try Again!
      </>)
    }
    navigate('/home')
  }

 

  return (
    
    <div className="App">
      <div classNameName="flex items-center justify-center">
        {!is_loading ? <section className="bg-white dark:bg-gray-900">
          <div className="py-8 px-4 mx-auto max-w-screen-xl text-center lg:py-16">
            <h1 className="mb-4 text-4xl font-extrabold tracking-tight leading-none text-gray-900 md:text-5xl lg:text-6xl dark:text-white">Let's Get Started</h1>
            <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-48 dark:text-gray-400">Looks like we don't have your Web ID on file yet. Go grab your Alta pass and find the 16 character code. Enter it below.</p>
            <p className="mb-8 text-lg font-normal text-gray-500 lg:text-xl sm:px-16 lg:px-48 dark:text-gray-400">Expect about a 30 second wait time while we grab your data.</p>
            <div className="flex flex-col space-y-4 sm:flex-row sm:justify-center sm:space-y-0 sm:space-x-4">
              <form className="flex max-w-md flex-col gap-4" onSubmit={saveWebId}>
                <div>
                  <div className="mb-2 block">
                    <Label htmlFor="webId" value="Enter Your Web ID found on your Alta Season Pass" />
                  </div>
                  <TextInput id="webId" placeholder="XXXXXXXX-XXX-XXX" required helperText={web_id_helper_text} />
                </div>
                <Button type="submit">Submit</Button>
              </form>
            </div>
          </div>
        </section> : <Spinner aria-label="Default status example" />}

        

      </div>

    </div>


  )
}
