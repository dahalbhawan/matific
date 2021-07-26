import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Form, Button, Container, Row, Col, Alert } from 'react-bootstrap'
import axios from 'axios'
import '../styles/Login.css'

function Login({ currentUser, loginCallback }) {
    let history = useHistory()
    
    const [userName, setUserName] = useState('')
    const [password, setPassword] = useState('')
    const [errorMessage, setErrorMessage] = useState('')

    const [user, setUser] = useState(currentUser)

    useEffect(() => {
        if (user){
            console.log(user)
            loginCallback(user)
            history.push('/scoreboard')
        }
    }, [user, history])

    const submitHandler = async (e) => {
        e.preventDefault()
        await axios
            .post('/auth/login/', {
                username: userName,
                password: password,
            })
            .then((response) => {
                setUser(response.data)
            }).catch(error => {
                setErrorMessage(error.message)
                console.log(error)
            })
    }

    return (
        <Container className="form-container">
            <Row className="justify-content-md-center">
                <Col xs={12} md={6}>
                    {errorMessage && <Alert variant="danger">{errorMessage}</Alert>}
                    <h3>Sign In</h3>
                    <hr></hr>
                    <Form onSubmit={submitHandler}>
                        <Form.Group className="mb-3" controlId="formBasicUsername">
                            <Form.Label>Username</Form.Label>
                            <Form.Control type="text" placeholder="Enter username" value={userName} onChange={e => setUserName(e.target.value)} />
                            <Form.Text className="text-muted">
                            </Form.Text>
                        </Form.Group>

                        <Form.Group className="mb-3" controlId="formBasicPassword">
                            <Form.Label>Password</Form.Label>
                            <Form.Control type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
                        </Form.Group>
                        <Button variant="primary" type="submit">
                            Login
                        </Button>
                    </Form>
                </Col>
            </Row>
        </Container>
    )
}

export default Login
