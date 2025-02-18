import React, { useState } from 'react';
import './App.css';
import playingCards from './playingCards'; // Import playing card images

const cardOptions = [
  "AS", "2S", "3S", "4S", "5S", "6S", "7S", "8S", "9S", "10S", "JS", "QS", "KS",
  "AC", "2C", "3C", "4C", "5C", "6C", "7C", "8C", "9C", "10C", "JC", "QC", "KC",
  "AD", "2D", "3D", "4D", "5D", "6D", "7D", "8D", "9D", "10D", "JD", "QD", "KD",
  "AH", "2H", "3H", "4H", "5H", "6H", "7H", "8H", "9H", "10H", "JH", "QH", "KH"
];

const App = () => {
  const [hand, setHand] = useState([]);
  const [community, setCommunity] = useState([]);
  const [opponent, setOpponent] = useState([]);
  const [odds, setOdds] = useState(null);

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
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ hand, community, opponent }),
      });

      if (!response.ok) {
        const errorResponse = await response.json();
        throw new Error(errorResponse.error || 'Unknown error occurred');
      }

      const data = await response.json();
      setOdds(data.odds);
    } catch (error) {
      console.error('Error calculating odds:', error.message);
    }
  };

  return (
    <div className="container">
      <h1>Poker Odds Calculator</h1>

      <div className="section">
        <h3>Your Hand</h3>
        <div className="card-container">
          {hand.map((card) => (
            <img
              key={card}
              src={playingCards[card]}
              alt={card}
              className="card smaller"
              onClick={() => handleRemove(card, setHand, hand)}
            />
          ))}
        </div>
        {hand.length < 2 && (
          <select onChange={(e) => handleSelect(e.target.value, setHand, 2, hand)}>
            <option value="">Select a card</option>
            {cardOptions.filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>{card}</option>
              ))}
          </select>
        )}
      </div>

      <div className="section">
        <h3>Community Cards</h3>
        <div className="card-container">
          {community.map((card) => (
            <img
              key={card}
              src={playingCards[card]}
              alt={card}
              className="card smaller"
              onClick={() => handleRemove(card, setCommunity, community)}
            />
          ))}
        </div>
        {community.length < 5 && (
          <select onChange={(e) => handleSelect(e.target.value, setCommunity, 5, community)}>
            <option value="">Select a card</option>
            {cardOptions.filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>{card}</option>
              ))}
          </select>
        )}
      </div>

      <div className="section">
        <h3>Opponent's Hand</h3>
        <div className="card-container">
          {opponent.map((card) => (
            <img
              key={card}
              src={playingCards[card]}
              alt={card}
              className="card smaller"
              onClick={() => handleRemove(card, setOpponent, opponent)}
            />
          ))}
        </div>
        {opponent.length < 2 && (
          <select onChange={(e) => handleSelect(e.target.value, setOpponent, 2, opponent)}>
            <option value="">Select a card</option>
            {cardOptions.filter((card) => !hand.includes(card) && !community.includes(card) && !opponent.includes(card))
              .map((card) => (
                <option key={card} value={card}>{card}</option>
              ))}
          </select>
        )}
      </div>

      <button className="calculate-btn" onClick={calculateOdds} disabled={hand.length !== 2 || opponent.length !== 2 || community.length < 3}>
        Calculate Odds
      </button>

      {odds && (
        <div className="odds-container">
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
