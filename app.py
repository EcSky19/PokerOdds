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
    ranks = sorted([card % 13 or 13 for card in all_cards], reverse=True)
    suits = [card // 13 for card in all_cards]

    rank_counts = Counter(ranks)
    suit_counts = Counter(suits)

    # Identify flush
    flush_suit = None
    for suit, count in suit_counts.items():
        if count >= 5:
            flush_suit = suit
            break#

    flush = flush_suit is not None
    flush_cards = sorted([rank for card, rank in zip(all_cards, ranks) if card // 13 == flush_suit], reverse=True) if flush else []

    # Identify straight
    sorted_ranks = sorted(set(ranks), reverse=True)
    straight = False
    straight_high_card = 0

    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i:i+5] == list(range(sorted_ranks[i], sorted_ranks[i]-5, -1)):
            straight = True
            straight_high_card = sorted_ranks[i]

    # Identify straight flush (must check before separate flush or straight)
    straight_flush = False
    straight_flush_high_card = 0
    if flush and len(flush_cards) >= 5:
        for i in range(len(flush_cards) - 4):
            if flush_cards[i:i+5] == list(range(flush_cards[i], flush_cards[i]-5, -1)):
                straight_flush = True
                straight_flush_high_card = flush_cards[i]
                break

    # Ensure proper ranking order
    if straight_flush:
        return (8, straight_flush_high_card)  # ✅ Highest rank: Straight Flush
    elif 4 in rank_counts.values():
        quad_rank = max(rank for rank, count in rank_counts.items() if count == 4)
        return (7, quad_rank)  # Four of a Kind
    elif sorted(rank_counts.values(), reverse=True)[:2] == [3, 2]:
        trip_rank = max(rank for rank, count in rank_counts.items() if count == 3)
        pair_rank = max(rank for rank, count in rank_counts.items() if count == 2)
        return (6, trip_rank, pair_rank)  # Full House
    elif flush:
        return (5, flush_cards[0])  # Flush
    elif straight:
        return (4, straight_high_card)  # Straight
    elif 3 in rank_counts.values():
        trip_rank = max(rank for rank, count in rank_counts.items() if count == 3)
        return (3, trip_rank)  # Three of a Kind
    elif list(rank_counts.values()).count(2) == 2:
        pair_ranks = sorted((rank for rank, count in rank_counts.items() if count == 2), reverse=True)
        return (2, pair_ranks[0], pair_ranks[1])  # Two Pair
    elif 2 in rank_counts.values():
        pair_rank = max(rank for rank, count in rank_counts.items() if count == 2)
        return (1, pair_rank)  # One Pair
    else:
        return (0, ranks[0])  # High Card



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
#