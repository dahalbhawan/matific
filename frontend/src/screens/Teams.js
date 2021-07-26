import React, {useState, useEffect} from 'react'
import axios from 'axios'
import { Link } from 'react-router-dom'

function Teams() {
    const [teams, setTeams] = useState([])
    
    useEffect(() => {
        fetchTeams()
    }, [])

    const fetchTeams = async () => {
        const response = await axios.get('/teams/')
        setTeams(response.data)
        console.log(response.data)
    }

    return (
        <div>
            {teams.map((team, i) => {
                return (<div><Link key={i} to={`/team/${team.id}`}>
                    {team.name}
                </Link></div>)
            })}
        </div>
    )
}

export default Teams

