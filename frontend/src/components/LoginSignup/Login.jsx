import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import './Login.css';

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await fetch("http://127.0.0.1:8000/users/login", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    email: email,
                    password: password
                }),
            })
            const result = await response.json();
            if (!response.ok) {
                throw new Error (`Login failed. Status code: ${result.detail}`)
            }
            console.log("Success: ", result)
            navigate("/home")
        } catch (error) {
            console.log("Error sending data. ", error)
        }
    }
    return (
        <div className="loginPage">
        <h1 className="logo">JitsHub</h1>
        <form className="loginBox" onSubmit={handleSubmit}>
        <div>

            <h2 className="loginHeader">Login</h2>
            <div className="inputGroup">
                <label>Email</label>
                <input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required/>
            </div>

            <div className="inputGroup">
                <label>Password</label>
                <input 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} 
                    required/>
            </div>
                <button className="loginButton" type="submit">Login</button>
        </div>
        <p>
            Don't have an account? <Link to="/register"><a>Create an account</a></Link>
        </p>
        </form>
        </div>
    )
}

export default Login
