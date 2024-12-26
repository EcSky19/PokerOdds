import random
from collections import Counter

# Define a deck of cards
def create_deck():
    suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    deck = [rank + ' of ' + suit for suit in suits for rank in ranks]
    return deck

def simulate_game(player_hand, opponent_hand, community_cards, num_simulations=10000):
    deck = create_deck()
    for card in player_hand + opponent_hand + community_cards:
        deck.remove(card)

    player_wins = 0
    opponent_wins = 0
    ties = 0

    for _ in range(num_simulations):
        random.shuffle(deck)

        remaining_community_cards = 5 - len(community_cards)
        additional_cards = deck[:remaining_community_cards]
        complete_community_cards = community_cards + additional_cards

        player_best = evaluate_hand(player_hand + complete_community_cards)
        opponent_best = evaluate_hand(opponent_hand + complete_community_cards)

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
    # Full poker hand ranking logic
    rank_values = {'2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10,
                   'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14}

    rank_counts = Counter(card.split()[0] for card in hand)
    suits = [card.split()[-1] for card in hand]

    # Check for flush
    suit_counts = Counter(suits)
    is_flush = any(count >= 5 for count in suit_counts.values())

    # Check for straight
    sorted_ranks = sorted(rank_values[rank] for rank in rank_counts.keys())
    is_straight = all(b == a + 1 for a, b in zip(sorted_ranks, sorted_ranks[1:]))

    # Determine hand strength
    if is_flush and is_straight:
        return 800 + max(sorted_ranks)  # Straight flush
    elif 4 in rank_counts.values():
        return 700 + get_rank_score(rank_counts, rank_values, 4)  # Four of a kind
    elif 3 in rank_counts.values() and 2 in rank_counts.values():
        return 600 + get_rank_score(rank_counts, rank_values, 3)  # Full house
    elif is_flush:
        flush_ranks = [rank_values[rank] for rank, suit in zip(rank_counts.keys(), suits) if suit_counts[suit] >= 5]
        return 500 + max(flush_ranks)  # Flush
    elif is_straight:
        return 400 + max(sorted_ranks)  # Straight
    elif 3 in rank_counts.values():
        return 300 + get_rank_score(rank_counts, rank_values, 3)  # Three of a kind
    elif list(rank_counts.values()).count(2) == 2:
        return 200 + get_rank_score(rank_counts, rank_values, 2, True)  # Two pair
    elif 2 in rank_counts.values():
        return 100 + get_rank_score(rank_counts, rank_values, 2)  # One pair
    else:
        return max(sorted_ranks)  # High card

def get_rank_score(rank_counts, rank_values, count, is_two_pair=False):
    # Helper to calculate score for pairs, three-of-a-kind, etc.
    if is_two_pair:
        pairs = [rank_values[rank] for rank, cnt in rank_counts.items() if cnt == 2]
        return sum(pairs) + max(pairs)
    for rank, cnt in rank_counts.items():
        if cnt == count:
            return rank_values[rank]

def main():
    print("Welcome to the Poker Odds Calculator!")
    
    player_hand = input("Enter your hand (e.g., 'Ace of Hearts, King of Diamonds'): ").split(', ')
    opponent_hand = input("Enter opponent's hand (e.g., 'Queen of Spades, Jack of Clubs'): ").split(', ')
    community_cards_input = input("Enter community cards (e.g., '10 of Hearts, Jack of Diamonds'), or leave blank if none: ").strip()
    community_cards = community_cards_input.split(', ') if community_cards_input else []

    player_odds, opponent_odds, tie_odds = simulate_game(player_hand, opponent_hand, community_cards)

    print(f"Your winning odds: {player_odds * 100:.2f}%")
    print(f"Opponent's winning odds: {opponent_odds * 100:.2f}%")
    print(f"Tie odds: {tie_odds * 100:.2f}%")

if __name__ == "__main__":
    main()
