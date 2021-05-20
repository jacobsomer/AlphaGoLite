import React, { Component } from "react";
import godash from "godash";
import { Goban } from "react-go-board";

export default class Room extends Component {
  constructor(props) {
    super(props);
    this.state = {
      votesToSkip: 2,
      guestCanPause: false,
      isHost: false,
    };
    this.roomCode = this.props.match.params.roomCode;
    this.getRoomDetails();

    this.handleCoordinateClick = this.handleCoordinateClick.bind(this);
  }

  getRoomDetails() {
    fetch("/api/get-room" + "?code=" + this.roomCode)
      .then((response) => response.json())
      .then((data) => {
        this.setState({
          votesToSkip: data.votes_to_skip,
          guestCanPause: data.guest_can_pause,
          isHost: data.is_host,
        });
      });
  }

  handleCoordinateClick(coordinate) {
    // http://duckpunch.github.io/godash/documentation/#coordinate
    coordinate;
  }
  render() {
    const board = new godash.Board(19);
    const annotations = [new godash.Coordinate(2, 2)];

    const divStyle = { width: "300px", height: "300px" };

    return (
      <div style={divStyle}>
        {/* <h3>{this.roomCode}</h3>
        <p>Votes: {this.state.votesToSkip}</p>
        <p>Guest Can Pause: {this.state.guestCanPause.toString()}</p>
        <p>Host: {this.state.isHost.toString()}</p> */}
        <Goban
          board={board}
          boardColor="#efefef"
          annotations={annotations}
          onCoordinateClick={this.handleCoordinateClick}
        />
        ;
      </div>
    );
  }
}
