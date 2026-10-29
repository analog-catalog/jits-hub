import React, { useState } from 'react'
import { Link } from 'react-router-dom'
import '../../App.css';

function Login() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");

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
        } catch (error) {
            console.log("Error sending data. ", error)
        }
    }
    return (
        <form onSubmit={handleSubmit}>
        <div>
            <h1>JitsHub</h1>

            <h2>Login</h2>
            <div>
                <label>Email</label>
                <input 
                    type="email" 
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required/>
            </div>

            <div>
                <label>Password</label>
                <input 
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)} 
                    required/>
            </div>

            <button type="submit">Login</button>
        </div>
        <p>
            Don't have an account?<Link to="/register"><button>Signup</button></Link>
        </p>
        </form>
    )
}

export default Login
