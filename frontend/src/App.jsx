import React from 'react'
import './App.css';
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Login from "./components/LoginSignup/loginsetup.jsx"
import SignUp from "./components/LoginSignup/signup.jsx"

function App() {
  return (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<SignUp />} />
    </Routes>
  </BrowserRouter>
  )
}

export default App
