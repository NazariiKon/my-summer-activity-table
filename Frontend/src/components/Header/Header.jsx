import { useState } from "react"
import checklist from './checklist.png';
import Button from "../Button/Button";

export default function Header() {
  return (
    <nav className="navbar navbar-dark bg-dark">
      <form className="form-inline p-2">
        <a className="navbar-brand" href="#">
          <img src={checklist} width="60" height="60" alt="" />
        </a>
        <Button></Button>
      </form>
    </nav>
  )
}