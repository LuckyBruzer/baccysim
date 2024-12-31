import random
import streamlit as st
import pandas as pd

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
def play_round(shoe, history, big_road):
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
        winner = determine_winner(player_total, banker_total)
    else:
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

    winner = determine_winner(player_total, banker_total)

    # Update history
    history.append({"Player": player_total, "Banker": banker_total, "Winner": winner})

    # Update Big Road
    if len(big_road) == 0 or winner != big_road[-1]["Winner"]:
        big_road.append({"Winner": winner, "Column": len(big_road) + 1, "Row": 1})
    else:
        big_road[-1]["Row"] += 1

    return player_hand, banker_hand, player_total, banker_total, history, big_road

# App initialization
st.set_page_config(page_title="Binker Baccarat", layout="wide")
shoe = create_shoe()
bankroll = 1000
history = []  # Store past hands
big_road = []  # Store Big Road data

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
        font-size: 20px;
        padding: 15px 30px;
    }
    .stButton>button:hover {
        background-color: #ff4d4d;
    }
    h1 {
        font-family: 'Courier New', monospace;
        color: gold;
        text-align: center;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Header
st.markdown("<h1>Binker Baccarat</h1>", unsafe_allow_html=True)

# Sidebar for bankroll and history toggle
with st.sidebar:
    st.header("Game Settings")
    st.markdown(f"### Bankroll: ${bankroll}")
    show_history = st.checkbox("Show Past Hands")
    show_big_road = st.checkbox("Show Big Road")

# Bet and deal section
bet_type = st.radio("Place Your Bet:", ["Player", "Banker", "Tie"], horizontal=True)
bet_amount = st.slider("Bet Amount:", min_value=10, max_value=bankroll, step=10)

if st.button("Deal"):
    player_hand, banker_hand, player_total, banker_total, history, big_road = play_round(shoe, history, big_road)

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

# Display past hands if toggled
if show_history and history:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Past Hands</h3>", unsafe_allow_html=True)
    for i, hand in enumerate(reversed(history), 1):
        st.markdown(f"**Round {i}:** Player Total: {hand['Player']}, Banker Total: {hand['Banker']}, Winner: {hand['Winner']}")

# Display Big Road if toggled
if show_big_road and big_road:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>Big Road</h3>", unsafe_allow_html=True)
    big_road_df = pd.DataFrame(big_road)
    st.dataframe(big_road_df)
