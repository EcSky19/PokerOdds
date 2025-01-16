from flask import Flask, jsonify, request
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Helper function: Simulate a poker game
def simulate_game(player_hand, community_cards):
    """
    Simulates a single poker game by generating a random opponent hand and remaining cards.
    This is a mock implementation; replace it with your actual poker logic.
    """
    deck = set(range(1, 53))  # Mock card IDs (1 to 52)
    used_cards = set(player_hand + community_cards)
    available_cards = list(deck - used_cards)

    if len(available_cards) < 7 - len(community_cards):  # Ensure enough cards remain
        raise ValueError("Not enough cards in the deck for a valid simulation.")

    # Generate opponent's hand
    opponent_hand = random.sample(available_cards, 2)
    available_cards = list(set(available_cards) - set(opponent_hand))

    # Complete the community cards if needed
    while len(community_cards) < 5:
        community_cards.append(available_cards.pop())

    # Simple win logic (replace with actual poker rules)
    player_score = sum(player_hand) + sum(community_cards)
    opponent_score = sum(opponent_hand) + sum(community_cards)
    return player_score > opponent_score

# Main function: Calculate odds
def calculate_poker_odds(hand, community):
    """
    Calculate the odds of winning using Monte Carlo Simulation.
    :param hand: List of two integers representing the player's hand cards.
    :param community: List of integers representing community cards (up to 5).
    :return: Win probability as a float.
    """
    total_simulations = 10000  # Number of Monte Carlo simulations
    wins = 0

    for _ in range(total_simulations):
        try:
            if simulate_game(hand, community[:]):  # Use a copy of the community cards
                wins += 1
        except ValueError:
            break

    return wins / total_simulations if total_simulations > 0 else 0.0

@app.route('/calculate-odds', methods=['POST'])
def calculate_odds():
    """
    API endpoint to calculate poker odds.
    Expects a JSON payload with 'hand' and 'community' card lists.
    """
    try:
        data = request.json
        hand = data.get('hand', [])
        community = data.get('community', [])
        
        if not hand or len(hand) != 2:
            return jsonify({"error": "Hand must contain exactly two cards."}), 400
        if len(community) > 5:
            return jsonify({"error": "Community cards cannot exceed five."}), 400

        odds = calculate_poker_odds(hand, community)
        return jsonify({
            "hand": hand,
            "community": community,
            "odds": f"{odds:.2%}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
