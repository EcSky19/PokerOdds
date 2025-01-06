import random
from collections import Counter
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/calculate-odds', methods=['POST'])
def calculate_odds():
    data = request.json
    player_hand = data.get('playerHand', [])
    opponent_hand = data.get('opponentHand', [])
    community_cards = data.get('communityCards', [])
    player_odds, opponent_odds, tie_odds = simulate_game(player_hand, opponent_hand, community_cards)
    return jsonify({
        "playerOdds": player_odds,
        "opponentOdds": opponent_odds,
        "tieOdds": tie_odds
    })

if __name__ == "__main__":
    app.run(debug=True)

def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    return [rank + ' of ' + suit for suit in suits for rank in ranks]

def simulate_game(player_hand, opponent_hand, community_cards, num_simulations=10000):
    deck = create_deck()
    for card in player_hand + community_cards:
        deck.remove(card)

    if opponent_hand:  # Remove opponent's cards if provided
        for card in opponent_hand:
            deck.remove(card)

    player_wins = 0
    opponent_wins = 0
    ties = 0

    for _ in range(num_simulations):
        random.shuffle(deck)

        remaining_community_cards = 5 - len(community_cards)
        additional_cards = deck[:remaining_community_cards]
        complete_community_cards = community_cards + additional_cards

        # If opponent hand is unknown, draw two random cards for the opponent
        if not opponent_hand:
            simulated_opponent_hand = deck[remaining_community_cards:remaining_community_cards + 2]
        else:
            simulated_opponent_hand = opponent_hand

        player_best = evaluate_hand(player_hand + complete_community_cards)
        opponent_best = evaluate_hand(simulated_opponent_hand + complete_community_cards)

        if player_best > opponent_best:
            player_wins += 1
        elif opponent_best > player_best:
            opponent_wins += 1
        else:
            ties += 1

    player_odds = player_wins / num_simulations
    opponent_odds = opponent_wins / num_simulations
    tie_odds = ties / num_simulations

    return player_odds, opponent_odds, tie_odds

def evaluate_hand(hand):
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    rank_counts = Counter(card.split()[0] for card in hand)
    suits = [card.split()[-1] for card in hand]
    suit_counts = Counter(suits)
    is_flush = any(count >= 5 for count in suit_counts.values())
    sorted_ranks = sorted(rank_values[rank] for rank in rank_counts.keys())
    is_straight = all(b == a + 1 for a, b in zip(sorted_ranks, sorted_ranks[1:]))

    if is_flush and is_straight:
        return 800 + max(sorted_ranks)  # Straight flush
    elif 4 in rank_counts.values():
        return 700 + max(sorted_ranks)  # Four of a kind
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return 600 + max(sorted_ranks)  # Full house
    elif is_flush:
        return 500 + max(sorted_ranks)  # Flush
    elif is_straight:
        return 400 + max(sorted_ranks)  # Straight
    elif 3 in rank_counts.values():
        return 300 + max(sorted_ranks)  # Three of a kind
    elif list(rank_counts.values()).count(2) == 2:
        return 200 + sum(sorted_ranks)  # Two pair
    elif 2 in rank_counts.values():
        return 100 + max(sorted_ranks)  # One pair
    else:
        return max(sorted_ranks)  # High card

def main():
    print("Welcome to the Poker Odds Calculator!")
    
    player_hand = input("Enter your hand (e.g., 'Ace of Hearts, King of Diamonds'): ").split(', ')
    opponent_hand_input = input("Enter opponent's hand (e.g., 'Queen of Spades, Jack of Clubs'), or leave blank if unknown: ").strip()
    community_cards_input = input("Enter community cards (e.g., '10 of Hearts, Jack of Diamonds'), or leave blank if none: ").strip()

    opponent_hand = opponent_hand_input.split(', ') if opponent_hand_input else []
    community_cards = community_cards_input.split(', ') if community_cards_input else []

    player_odds, opponent_odds, tie_odds = simulate_game(player_hand, opponent_hand, community_cards)

    print(f"Your winning odds: {player_odds * 100:.2f}%")
    print(f"Opponent's winning odds: {opponent_odds * 100:.2f}%")
    print(f"Tie odds: {tie_odds * 100:.2f}%")

if __name__ == "__main__":
    main()
