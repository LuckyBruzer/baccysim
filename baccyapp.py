import random
import streamlit as st
import time

# Initialize the shoe (6 decks of cards with suits)
def create_shoe():
    ranks = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0]  # Card values
    suits = ["♠", "♥", "♦", "♣"]  # Card suits
    shoe = [{"rank": rank, "suit": suit} for rank in ranks for suit in suits] * 6  # 6 decks
    random.shuffle(shoe)
    return shoe

# Deal one card
def deal_card(shoe):
    return shoe.pop(0)

# Calculate the hand total
def calculate_total(hand):
    return sum(card["rank"] for card in hand) % 10

# Format cards for display
def format_cards(hand):
    return [f'{card["rank"] if card["rank"] != 0 else "10"}{card["suit"]}' for card in hand]

# Determine the winner
def determine_winner(player_total, banker_total):
    if player_total > banker_total:
        return "Player"
    elif banker_total > player_total:
        return "Banker"
    else:
        return "Tie"

# Baccarat game logic
def play_round(shoe):
    player_hand = []
    banker_hand = []

    # First cards
    player_hand.append(deal_card(shoe))
    banker_hand.append(deal_card(shoe))

    # Second cards
    player_hand.append(deal_card(shoe))
    banker_hand.append(deal_card(shoe))

    player_total = calculate_total(player_hand)
    banker_total = calculate_total(banker_hand)

    # Check for natural win
    if player_total in [8, 9] or banker_total in [8, 9]:
        return player_hand, banker_hand, player_total, banker_total

    # Player third card rule
    if player_total <= 5:
        player_hand.append(deal_card(shoe))
        player_total = calculate_total(player_hand)

    # Banker third card rule
    if banker_total <= 2:
        banker_hand.append(deal_card(shoe))
    elif banker_total == 3 and (len(player_hand) < 3 or player_hand[2]["rank"] != 8):
        banker_hand.append(deal_card(shoe))
    elif banker_total == 4 and (len(player_hand) < 3 or 2 <= player_hand[2]["rank"] <= 7):
        banker_hand.append(deal_card(shoe))
    elif banker_total == 5 and (len(player_hand) < 3 or 4 <= player_hand[2]["rank"] <= 7):
        banker_hand.append(deal_card(shoe))
    elif banker_total == 6 and (len(player_hand) < 3 or player_hand[2]["rank"] in [6, 7]):
        banker_hand.append(deal_card(shoe))

    banker_total = calculate_total(banker_hand)
    return player_hand, banker_hand, player_total, banker_total

# App initialization
st.set_page_config(page_title="Casino-Style Baccarat", layout="wide")
shoe = create_shoe()
bankroll = 1000

# Styling
st.markdown(
    """
    <style>
    body {
        background-color: #004d00;
        color: white;
    }
    .stButton>button {
        color: white;
        background-color: #b30000;
        border: none;
        font-size: 16px;
        padding: 10px 20px;
    }
    .stButton>button:hover {
        background-color: #ff4d4d;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Game layout
st.markdown(f"<h1 style='text-align: center; color: gold;'>Welcome to Casino-Style Baccarat</h1>", unsafe_allow_html=True)
st.markdown(f"<h3 style='text-align: center; color: white;'>Your Bankroll: ${bankroll}</h3>", unsafe_allow_html=True)

bet_type = st.radio("Place Your Bet:", ["Player", "Banker", "Tie"], horizontal=True)
bet_amount = st.slider("Bet Amount:", min_value=10, max_value=bankroll, step=10)

if st.button("Deal"):
    player_hand, banker_hand, player_total, banker_total = play_round(shoe)

    # Determine the winner
    winner = "Player" if player_total > banker_total else "Banker" if banker_total > player_total else "Tie"

    # Display cards
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align: center;'>Results</h3>", unsafe_allow_html=True)
    st.markdown(f"<b>Player Hand:</b> {', '.join(format_cards(player_hand))} | Total: {player_total}")
    st.markdown(f"<b>Banker Hand:</b> {', '.join(format_cards(banker_hand))} | Total: {banker_total}")
    st.markdown(f"<b>Winner:</b> {winner}")

    # Update bankroll
    if winner == bet_type:
        payout = bet_amount * 8 if winner == "Tie" else bet_amount
        bankroll += payout
        st.success(f"You won ${payout}!")
    else:
        bankroll -= bet_amount
        st.error(f"You lost ${bet_amount}!")

    st.markdown(f"<h3 style='text-align: center; color: white;'>Updated Bankroll: ${bankroll}</h3>", unsafe_allow_html=True)
