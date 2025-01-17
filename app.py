from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

# Convert card strings to numeric IDs for easier processing (mock example)
def card_to_id(card):
    suits = {'S': 0, 'C': 13, 'D': 26, 'H': 39}
    ranks = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    rank = ''.join(filter(str.isdigit, card)) or card[0]
    suit = card[-1]
    return ranks[rank] + suits[suit]

# Simulate a poker game
def simulate_game(player_hand, community_cards, opponent_hand):
    deck = set(range(1, 53))
    used_cards = set(player_hand + community_cards + opponent_hand)
    available_cards = list(deck - used_cards)

    if len(available_cards) < 5 - len(community_cards):
        raise ValueError("Not enough cards in the deck for a valid simulation.")

    # Fill in remaining community cards if needed
    while len(community_cards) < 5:
        community_cards.append(available_cards.pop())

    # Simple win logic (replace with actual poker evaluation logic)
    player_score = sum(player_hand) + sum(community_cards)
    opponent_score = sum(opponent_hand) + sum(community_cards)
    return player_score > opponent_score

# Main function: Calculate odds
def calculate_poker_odds(player_hand, community_cards, opponent_hand):
    total_simulations = 10000
    wins = 0

    for _ in range(total_simulations):
        try:
            if simulate_game(player_hand[:], community_cards[:], opponent_hand[:]):
                wins += 1
        except ValueError:
            break

    return wins / total_simulations if total_simulations > 0 else 0.0

@app.route('/calculate-odds', methods=['POST'])
def calculate_odds():
    try:
        data = request.json
        hand = data.get('hand', [])
        community = data.get('community', [])
        opponent = data.get('opponent', [])

        # Validate inputs
        if not hand or len(hand) != 2:
            return jsonify({"error": "Hand must contain exactly two cards."}), 400
        if len(community) > 5:
            return jsonify({"error": "Community cards cannot exceed five."}), 400
        if not opponent or len(opponent) != 2:
            return jsonify({"error": "Opponent hand must contain exactly two cards."}), 400

        # Convert cards to IDs
        player_hand = [card_to_id(card) for card in hand]
        community_cards = [card_to_id(card) for card in community]
        opponent_hand = [card_to_id(card) for card in opponent]

        # Calculate odds
        odds = calculate_poker_odds(player_hand, community_cards, opponent_hand)

        return jsonify({
            "hand": hand,
            "community": community,
            "opponent": opponent,
            "odds": f"{odds:.2%}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
