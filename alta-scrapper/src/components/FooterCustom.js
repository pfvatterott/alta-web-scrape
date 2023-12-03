import React from 'react'
import { Footer } from 'flowbite-react';

export default function FooterCustom() {
  return (
    <Footer container className="fixed bottom-0">
      <div className="w-full text-center">
        <div className="w-full justify-between sm:flex sm:items-center sm:justify-between sticky">
          <Footer.LinkGroup>
            <Footer.Link href="#">About</Footer.Link>
            <Footer.Link href="#">Privacy Policy</Footer.Link>
            <Footer.Link href="#">Licensing</Footer.Link>
            <Footer.Link href="#">Contact</Footer.Link>
          </Footer.LinkGroup>
        </div>
        <Footer.Divider />
        <Footer.Copyright href="#" by="Paul Vatterott" year={2023} />
      </div>
    </Footer>
  )
}
