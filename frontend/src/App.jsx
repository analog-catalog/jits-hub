import React from 'react'
import {BrowserRouter, Routes, Route} from 'react-router-dom'
import Login from "./components/LoginSignup/Login.jsx"
import SignUp from "./components/LoginSignup/signup.jsx"
import Home from "./components/JitshubMemberArea.jsx"

function App() {
  return (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Login />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<SignUp />} />
      <Route path="/home" element={<Home />} />
    </Routes>
  </BrowserRouter>
  )
}

export default App
