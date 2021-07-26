import React, { useState, useEffect } from 'react'
import { BrowserRouter as Router, Route } from 'react-router-dom'
import './App.css';
import Header from './components/Header';
import { Container } from 'react-bootstrap';
import Login from './screens/Login';
import Scoreboard from './screens/Scoreboard';
import Teams from './screens/Teams';
import Team from './screens/Team';

function App() {
  const [user, setUser] = useState(JSON.parse(localStorage.getItem('user')))

  useEffect(() => {
    console.log(user)
  }, [user])

  const loginCallback = (loggedInUser) => {
    localStorage.setItem('user', JSON.stringify(loggedInUser))
    setUser(loggedInUser)
  }

  const logoutCallback = () => {
    localStorage.removeItem('user')
    setUser(null)
  }

  return (
    <Router>
      <Header logoutCallback={logoutCallback} currentUser={user} />
      <main className='py-3'>
        <Container>
          <Route exact path='/' render={(props) => <Login {...props} currentUser={user} loginCallback={loginCallback} />} />
          <Route path='/scoreboard' render={(props) => <Scoreboard {...props} currentUser={user} />} />
          <Route path='/teams' component={Teams} />
          <Route path='/team/:id' component = {Team} />
        </Container>
      </main>
    </Router>
  );
}

export default App;
