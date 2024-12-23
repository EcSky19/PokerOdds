import itertools
import random
from collections import Counter

# Constants
RANKS = "23456789TJQKA"
SUITS = "hdcs"  # hearts, diamonds, clubs, spades
DECK = [r + s for r in RANKS for s in SUITS]

# Hand Rankings
HAND_RANKS = {
    "High Card": 0,
    "One Pair": 1,
    "Two Pair": 2,
    "Three of a Kind": 3,
    "Straight": 4,
    "Flush": 5,
    "Full House": 6,
    "Four of a Kind": 7,
    "Straight Flush": 8,
    "Royal Flush": 9,
}

# Helper Functions
def create_deck(exclude=[]):
    """Create a deck of cards excluding the specified cards."""
    return [card for card in DECK if card not in exclude]

def deal_hands(deck, num_hands=2, cards_per_hand=2):
    """Deal hands for the players."""
    hands = [random.sample(deck, cards_per_hand) for _ in range(num_hands)]
    remaining_deck = list(set(deck) - set(itertools.chain.from_iterable(hands)))
    return hands, remaining_deck

def evaluate_hand(cards):
    """Evaluate a poker hand and return its rank and the highest cards."""
    def is_flush(cards):
        suits = [c[1] for c in cards]
        return len(set(suits)) == 1

    def is_straight(cards):
        ranks = sorted([RANKS.index(c[0]) for c in cards])
        return all(ranks[i] + 1 == ranks[i + 1] for i in range(len(ranks) - 1))

    def count_ranks(cards):
        rank_counts = Counter(c[0] for c in cards)
        return rank_counts.most_common()

    ranks = count_ranks(cards)
    is_flush_flag = is_flush(cards)
    is_straight_flag = is_straight(cards)

    if is_flush_flag and is_straight_flag:
        return ("Straight Flush", cards)
    if ranks[0][1] == 4:
        return ("Four of a Kind", cards)
    if ranks[0][1] == 3 and ranks[1][1] == 2:
        return ("Full House", cards)
    if is_flush_flag:
        return ("Flush", cards)
    if is_straight_flag:
        return ("Straight", cards)
    if ranks[0][1] == 3:
        return ("Three of a Kind", cards)
    if ranks[0][1] == 2 and ranks[1][1] == 2:
        return ("Two Pair", cards)
    if ranks[0][1] == 2:
        return ("One Pair", cards)
    return ("High Card", cards)

def simulate_odds(hole_cards, community_cards, num_opponents=1, iterations=1000):
    """Simulate poker odds using Monte Carlo."""
    deck = create_deck(exclude=hole_cards + community_cards)
    wins, ties, losses = 0, 0, 0

    for _ in range(iterations):
        random.shuffle(deck)
        # Simulate community cards
        missing_community = 5 - len(community_cards)
        simulated_community = community_cards + deck[:missing_community]

        # Simulate opponent hands
        opponents = [deck[missing_community + i * 2: missing_community + i * 2 + 2] for i in range(num_opponents)]
        remaining_deck = deck[missing_community + num_opponents * 2:]

        # Evaluate player hand
        player_hand = evaluate_hand(hole_cards + simulated_community)

        # Evaluate opponent hands
        opponent_hands = [evaluate_hand(opponent + simulated_community) for opponent in opponents]

        # Compare hands
        player_wins = sum(player_hand > opp_hand for opp_hand in opponent_hands)
        player_ties = sum(player_hand == opp_hand for opp_hand in opponent_hands)

        if player_wins == num_opponents:
            wins += 1
        elif player_ties > 0:
            ties += 1
        else:
            losses += 1

    total = wins + ties + losses
    return {
        "Wins": wins / total * 100,
        "Ties": ties / total * 100,
        "Losses": losses / total * 100
    }

# Main Function
def main():
    # Input: Player hole cards and known community cards
    hole_cards = input("Enter your hole cards (e.g., 'Ah Kd'): ").split()
    community_cards = input("Enter community cards (if any, e.g., '2h 3d 4s'): ").split()
    num_opponents = int(input("Enter number of opponents: "))

    # Simulate odds
    results = simulate_odds(hole_cards, community_cards, num_opponents)
    
    # Output results
    print("\n--- Poker Odds ---")
    for outcome, percentage in results.items():
        print(f"{outcome}: {percentage:.2f}%")

# Run the Program
if __name__ == "__main__":
    main()
