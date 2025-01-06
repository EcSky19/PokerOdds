import React, { useState } from "react";
import axios from "axios";

const App = () => {
  const [playerHand, setPlayerHand] = useState(["", ""]);
  const [opponentHand, setOpponentHand] = useState(["", ""]);
  const [communityCards, setCommunityCards] = useState(["", "", "", "", ""]);
  const [results, setResults] = useState(null);

  const handleCardChange = (setFunction, index, value) => {
    setFunction((prev) => {
      const newSelection = [...prev];
      newSelection[index] = value;
      return newSelection;
    });
  };

  const calculateOdds = async () => {
    try {
      const response = await axios.post("http://localhost:5000/calculate-odds", {
        playerHand,
        opponentHand,
        communityCards,
      });
      setResults(response.data);
    } catch (error) {
      console.error("Error calculating odds:", error);
    }
  };

  const renderCardSelector = (label, hand, setFunction, count) => (
    <div>
      <h3>{label}</h3>
      {[...Array(count)].map((_, i) => (
        <select
          key={i}
          value={hand[i] || ""}
          onChange={(e) => handleCardChange(setFunction, i, e.target.value)}
        >
          <option value="">Select Card</option>
          {["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
            .map((rank) =>
              ["Hearts", "Diamonds", "Clubs", "Spades"].map(
                (suit) => `${rank} of ${suit}`
              )
            )
            .flat()
            .map((card) => (
              <option key={card} value={card}>
                {card}
              </option>
            ))}
        </select>
      ))}
    </div>
  );

  return (
    <div>
      <h1>Poker Odds Calculator</h1>
      {renderCardSelector("Player Hand", playerHand, setPlayerHand, 2)}
      {renderCardSelector("Opponent Hand", opponentHand, setOpponentHand, 2)}
      {renderCardSelector("Community Cards", communityCards, setCommunityCards, 5)}
      <button onClick={calculateOdds}>Calculate Odds</button>
      {results && (
        <div>
          <h2>Results</h2>
          <p>Player Odds: {results.playerOdds * 100}%</p>
          <p>Opponent Odds: {results.opponentOdds * 100}%</p>
          <p>Tie Odds: {results.tieOdds * 100}%</p>
        </div>
      )}
    </div>
  );
};

export default App;
