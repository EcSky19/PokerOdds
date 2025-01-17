import React, { useState } from 'react';

const App = () => {
  const [hand, setHand] = useState([]);
  const [community, setCommunity] = useState([]);
  const [opponent, setOpponent] = useState([]);
  const [odds, setOdds] = useState(null);
  const [stage, setStage] = useState(0); // 0: pre-flop, 3: flop, 4: turn, 5: river

  const cardOptions = [
    "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
    "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
    "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
    "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"
  ];

  const handleSelect = (value, setCards, maxCards, cards) => {
    if (value && !cards.includes(value) && cards.length < maxCards) {
      setCards([...cards, value]);
    }
  };

  const handleRemove = (value, setCards, cards) => {
    setCards(cards.filter((card) => card !== value));
  };

  const calculateOdds = async () => {
    try {
      console.log('Sending data to backend:', { hand, community, opponent });
      const response = await fetch('http://127.0.0.1:5000/calculate-odds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ hand, community, opponent }),
      });

      console.log('Response status:', response.status);
      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.error || 'Unknown error occurred');
      }

      const data = await response.json();
      console.log('Odds received:', data);
      setOdds(data.odds);
    } catch (error) {
      console.error('Error calculating odds:', error.message);
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "20px" }}>
      <h1>Poker Odds Calculator</h1>

      <div>
        <h3>Select Your Hand (2 cards):</h3>
        {hand.map((card, index) => (
          <div key={index}>
            <span>{card}</span>
            <button onClick={() => handleRemove(card, setHand, hand)}>Remove</button>
          </div>
        ))}
        {hand.length < 2 && (
          <select
            onChange={(e) => {
              handleSelect(e.target.value, setHand, 2, hand);
              e.target.value = "";
            }}
          >
            <option value="">Select a card</option>
            {cardOptions
              .filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>
                  {card}
                </option>
              ))}
          </select>
        )}
      </div>

      <div>
        <h3>Select Community Cards ({stage} cards):</h3>
        {community.map((card, index) => (
          <div key={index}>
            <span>{card}</span>
            <button onClick={() => handleRemove(card, setCommunity, community)}>Remove</button>
          </div>
        ))}
        {community.length < stage && (
          <select
            onChange={(e) => {
              handleSelect(e.target.value, setCommunity, stage, community);
              e.target.value = "";
            }}
          >
            <option value="">Select a card</option>
            {cardOptions
              .filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>
                  {card}
                </option>
              ))}
          </select>
        )}
      </div>

      <div>
        <h3>Select Opponent's Hand (2 cards):</h3>
        {opponent.map((card, index) => (
          <div key={index}>
            <span>{card}</span>
            <button onClick={() => handleRemove(card, setOpponent, opponent)}>Remove</button>
          </div>
        ))}
        {opponent.length < 2 && (
          <select
            onChange={(e) => {
              handleSelect(e.target.value, setOpponent, 2, opponent);
              e.target.value = "";
            }}
          >
            <option value="">Select a card</option>
            {cardOptions
              .filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>
                  {card}
                </option>
              ))}
          </select>
        )}
      </div>

      <div style={{ marginTop: "20px" }}>
        <button
          onClick={() => setStage(0)}
          disabled={stage === 0}
          style={{ margin: "5px" }}
        >
          Pre-Flop
        </button>
        <button
          onClick={() => setStage(3)}
          disabled={stage === 3}
          style={{ margin: "5px" }}
        >
          Flop
        </button>
        <button
          onClick={() => setStage(4)}
          disabled={stage === 4}
          style={{ margin: "5px" }}
        >
          Turn
        </button>
        <button
          onClick={() => setStage(5)}
          disabled={stage === 5}
          style={{ margin: "5px" }}
        >
          River
        </button>
      </div>

      <button
        onClick={calculateOdds}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
        disabled={hand.length !== 2 || opponent.length !== 2 || community.length !== stage}
      >
        Calculate Odds
      </button>

      {odds && (
        <div style={{ marginTop: "20px" }}>
          <h2>Calculated Odds</h2>
          <p>Win: {odds.win}</p>
          <p>Tie: {odds.tie}</p>
          <p>Loss: {odds.loss}</p>
        </div>
      )}
    </div>
  );
};

export default App;
