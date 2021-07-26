import React, { useState, useEffect } from 'react'
import axios from 'axios'

function Scoreboard() {
    const [matches, setMatches] = useState([])
    const match_type = (number) => {
        if (number === 1)
            return 'Qualifiers'
        else if (number === 2)
            return 'Quarter Final'
        else if (number === 3)
            return 'Semi-final'
        else
            return 'Final'
    }
    useEffect(() => {
        fetchScoreboard()
    }, [])

    const fetchScoreboard = async () => {
        const response = await axios.get('/matches/')
        setMatches(response.data)
        console.log(response.data)
    }

    return (
        <div>
            <h1>Scoreboard</h1>
            <hr></hr>
            { matches.map((match, i) => {
                return (
                    <div key={i}>
                        {match_type(match.competition.type)}: {match.first_team.name} vs {match.second_team.name}, winner: {match.winner ? match.first_team.name : match.second_team.name}
                        <hr></hr>
                    </div>
                    )
                } ) }
        </div>
    )
}

export default Scoreboard
