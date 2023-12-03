import React from 'react'
import { Navbar } from 'flowbite-react';

export default function NavBar() {
  return (
    <Navbar fluid rounded>
      <Navbar.Brand  href="https://flowbite-react.com">
        <span className="self-center whitespace-nowrap text-xl font-semibold dark:text-white">AltaTracker</span>
      </Navbar.Brand>
      <Navbar.Toggle />
      <Navbar.Collapse>
        <Navbar.Link href="/home" active>
          Home
        </Navbar.Link>
        <Navbar.Link href="#">Leader Boards</Navbar.Link>
      </Navbar.Collapse>
    </Navbar>
  )
}
