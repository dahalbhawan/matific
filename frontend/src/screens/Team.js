import React, { useEffect, useState } from 'react'
import axios from 'axios'
import Player from '../components/Player'

function Team({ match }) {
    const [team, setTeam] = useState({})
    const [teamPlayers, setTeamPlayers] = useState([])

    useEffect(() => {
        fetchPlayers()
    }, [team])

    const fetchPlayers = async () => {
        const response = await axios.get('/players/')
        const players = response.data
        for(let i=0; i<players.length; i++){
            if(players[i].team.id === team.id){
                setTeamPlayers((teamPlayers) => [...teamPlayers, players[i]])
                console.log(players[i])
            }
        }
    }

    useEffect(() => {
        fetchTeamDetails()
    }, [match])

    const fetchTeamDetails = async () => {
        const response = await axios.get(`/teams/${match.params.id}/`)
        setTeam(response.data)
    }

    return (
        <div>
            <div>Team: {team?.name} </div>
            <hr></hr>
            <div>Average score: {team?.average_score} </div>
            <div>Coach: {team.coach?.user.username}</div>
            <hr></hr>
            <h4>Players</h4>
            <hr></hr>
            {teamPlayers?.map((player, i) => (
                <>
                    <Player key={i} username={player.user?.username} average_score={player.average_score} number_of_caps={player.number_of_caps} />
                    <hr></hr>
                </>
            ))}
        </div>
    )
}

export default Team
