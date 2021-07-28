import React, { useState, useEffect } from 'react'
import { useHistory } from 'react-router-dom'
import { Container, Navbar, Nav, Button } from 'react-bootstrap'
import { LinkContainer } from 'react-router-bootstrap' 
import axios from 'axios'

function Header({ currentUser, logoutCallback  }) {
    const [user, setUser] = useState(currentUser)
    const [team, setTeam] = useState({})
    const history = useHistory()

    useEffect(() => {
        setUser(currentUser)
    }, [user, currentUser])

    useEffect(() => {
        getTeam()
    }, [user])

    const logoutHandler = () => {
        setUser(null)
        logoutCallback()
        history.push('/')
    }

    const getTeam = async () => {
        const response = await axios.get('/coaches/')
        const coaches = response.data
        for(let i=0; i<coaches.length; i++) {
            if (coaches[i].user.id === user?.id){
                setTeam(coaches[i].team)
            }
        }
        
    }

    return (
        <Navbar bg="primary" variant="dark">
            <Container>
                <Navbar.Brand href="#home">BasketballWay</Navbar.Brand>
                    <Nav className="me-auto">
                        { user ? (
                            <>
                                <Nav.Link>{user.username}</Nav.Link>
                                <LinkContainer to="/scoreboard">
                                    <Nav.Link>Scoreboard</Nav.Link>
                                </LinkContainer>
                            </>
                            ): null 
                        }
                        { user&&user.role===2 ?  (
                            <LinkContainer to={`/team/${team}`}>
                                <Nav.Link>My Team</Nav.Link>
                            </LinkContainer>
                        ): null }
                        { user&&user.role===3 ?  (
                            <LinkContainer to='/teams'>
                                <Nav.Link>Teams</Nav.Link>
                            </LinkContainer>
                        ): null }
                        { user ? (
                                <Nav.Link><Button variant="secondary" size="sm" onClick={logoutHandler}>Sign Out</Button></Nav.Link>
                        ) : null
                    }
                    </Nav>
            </Container>
        </Navbar>
    )
}

export default Header
