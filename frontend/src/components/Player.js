import React from 'react'

function Player(props) {
    return (
        <div>
            <div>Name: {props.username}</div>
            <div>Average Score: {props.average_score}</div>
            <div>Number of Games: {props.number_of_caps}</div>
        </div>
    )
}

export default Player
