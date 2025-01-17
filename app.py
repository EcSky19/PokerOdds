from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from collections import Counter

app = Flask(__name__)
CORS(app)

def card_to_id(card):
    suits = {'S': 0, 'C': 13, 'D': 26, 'H': 39}
    ranks = {'A': 14, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
             '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    rank = ''.join(filter(str.isdigit, card)) or card[0]
    suit = card[-1]
    return ranks[rank] + suits[suit]

def evaluate_hand(hand, community):
    all_cards = hand + community
    ranks = [card % 13 or 13 for card in all_cards]
    suits = [card // 13 for card in all_cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    # Check for flush
    flush_suit = None
    for suit, count in suit_counts.items():
        if count >= 5:
            flush_suit = suit
            break

    flush = False
    flush_high_card = 0
    if flush_suit is not None:
        flush = True
        flush_cards = [rank for card, rank in zip(all_cards, ranks) if card // 13 == flush_suit]
        flush_high_card = max(flush_cards)

    # Check for straight
    sorted_ranks = sorted(set(ranks))
    straight = False
    straight_high_card = 0
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i:i+5] == list(range(sorted_ranks[i], sorted_ranks[i]+5)):
            straight = True
            straight_high_card = sorted_ranks[i+4]

    # Basic scoring logic
    if flush and straight:
        return (8, flush_high_card)  # Straight flush
    elif 4 in rank_counts.values():
        quad_rank = max(rank for rank, count in rank_counts.items() if count == 4)
        return (7, quad_rank)  # Four of a kind
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        trip_rank = max(rank for rank, count in rank_counts.items() if count == 3)
        pair_rank = max(rank for rank, count in rank_counts.items() if count == 2)
        return (6, trip_rank, pair_rank)  # Full house
    elif flush:
        return (5, flush_high_card)  # Flush
    elif straight:
        return (4, straight_high_card)  # Straight
    elif 3 in rank_counts.values():
        trip_rank = max(rank for rank, count in rank_counts.items() if count == 3)
        return (3, trip_rank)  # Three of a kind
    elif list(rank_counts.values()).count(2) == 2:
        pair_ranks = sorted((rank for rank, count in rank_counts.items() if count == 2), reverse=True)
        return (2, pair_ranks[0], pair_ranks[1])  # Two pair
    elif 2 in rank_counts.values():
        pair_rank = max(rank for rank, count in rank_counts.items() if count == 2)
        return (1, pair_rank)  # One pair
    else:
        return (0, max(ranks))  # High card

def simulate_game(player_hand, community_cards, opponent_hand):
    deck = set(range(1, 53))
    used_cards = set(player_hand + community_cards + opponent_hand)
    available_cards = list(deck - used_cards)

    while len(community_cards) < 5:
        drawn_card = random.choice(available_cards)
        community_cards.append(drawn_card)
        available_cards.remove(drawn_card)

    # Evaluate hands
    player_score = evaluate_hand(player_hand, community_cards)
    opponent_score = evaluate_hand(opponent_hand, community_cards)

    if player_score > opponent_score:
        return "win"
    elif player_score == opponent_score:
        return "tie"
    else:
        return "loss"

def calculate_poker_odds(player_hand, community_cards, opponent_hand):
    total_simulations = 10000
    results = {"win": 0, "tie": 0, "loss": 0}

    for _ in range(total_simulations):
        try:
            outcome = simulate_game(player_hand[:], community_cards[:], opponent_hand[:])
            results[outcome] += 1
        except ValueError:
            break

    total = sum(results.values())
    return {key: value / total for key, value in results.items()}

@app.route('/calculate-odds', methods=['POST'])
def calculate_odds():
    try:
        data = request.json
        hand = data.get('hand', [])
        community = data.get('community', [])
        opponent = data.get('opponent', [])

        player_hand = [card_to_id(card) for card in hand]
        community_cards = [card_to_id(card) for card in community]
        opponent_hand = [card_to_id(card) for card in opponent]

        odds = calculate_poker_odds(player_hand, community_cards, opponent_hand)

        return jsonify({"odds": {
            "win": f"{odds['win']:.2%}",
            "tie": f"{odds['tie']:.2%}",
            "loss": f"{odds['loss']:.2%}"
        }})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
