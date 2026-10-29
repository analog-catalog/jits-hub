import React, { useState } from 'react'
import {useNavigate, Link} from 'react-router-dom'
import '../../App.css';

function SignUp() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [name, setName] = useState("");
    const navigate = useNavigate();
    const handleSubmit = async (e) => {
        e.preventDefault()
        try {
            const response = await fetch("http://127.0.0.1:8000/users/register", {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    password: password
                }),
            })
            const result = await response.json();
            if (!response.ok) {
                throw new Error (`Signup failed. Status code: ${result.detail}`)
            }
            navigate('/')
        } catch (error) {
            console.log("Error sending data. ", error)
        }
    }
    return (
        <form onSubmit={handleSubmit}>
        <div>
            <h1>JitsHub</h1>

            <h2></h2>
            <div>
                <label>Name</label>
                <input 
                    type="name" 
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    required/>
            </div>
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

            <button type="submit">Signup</button>
        </div>
        <p>
            Already have an account<Link to="/login"><button>Login</button></Link>
        </p>
        </form>
    )
}

export default SignUp
