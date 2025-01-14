import React, { useState } from 'react';

const App = () => {
  const [hand, setHand] = useState([]);
  const [community, setCommunity] = useState([]);
  const [odds, setOdds] = useState(null);

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
      const response = await fetch('http://127.0.0.1:5000/calculate-odds', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ hand, community }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setOdds(data.odds);
    } catch (error) {
      console.error('Error calculating odds:', error);
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
              .filter((card) => !hand.includes(card) && !community.includes(card))
              .map((card) => (
                <option key={card} value={card}>
                  {card}
                </option>
              ))}
          </select>
        )}
      </div>

      <div>
        <h3>Select Community Cards (up to 5):</h3>
        {community.map((card, index) => (
          <div key={index}>
            <span>{card}</span>
            <button onClick={() => handleRemove(card, setCommunity, community)}>Remove</button>
          </div>
        ))}
        {community.length < 5 && (
          <select
            onChange={(e) => {
              handleSelect(e.target.value, setCommunity, 5, community);
              e.target.value = "";
            }}
          >
            <option value="">Select a card</option>
            {cardOptions
              .filter((card) => !hand.includes(card) && !community.includes(card))
              .map((card) => (
                <option key={card} value={card}>
                  {card}
                </option>
              ))}
          </select>
        )}
      </div>

      <button
        onClick={calculateOdds}
        style={{
          marginTop: "20px",
          padding: "10px 20px",
          fontSize: "16px",
          cursor: "pointer",
        }}
        disabled={hand.length !== 2 || community.length === 0}
      >
        Calculate Odds
      </button>

      {odds && (
        <div style={{ marginTop: "20px" }}>
          <h2>Calculated Odds</h2>
          <p>{odds}</p>
        </div>
      )}
    </div>
  );
};

export default App;
