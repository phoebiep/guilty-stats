import psycopg2
import numpy as np
from decimal import Decimal

conn = psycopg2.connect(
    host="localhost",
    database="ggst-stats",
    user="postgres",
    password="password"
)

chars = ("SO","KY","MA","AX","CH","PO","FA","MI","ZA","RA","LE","NA","GI","AN","IN","GO","JC","HA","BA","TE","BI","SI")
p1char_count = [0] * len(chars)
p2char_count = [0] * len(chars)

def get_p1char_count(chars, p1char_count):
    # get every player one character form the database
    cur = conn.cursor()
    cur.execute("SELECT player1_char FROM match_temp")
    rows = cur.fetchall()

    # updates the character count every time that character is found
    for row in rows:
        char_index = row[0]
        if char_index < len(chars):
            p1char_count[char_index] += 1
    ### Print the amount per character
    # for i in range(len(chars)):
    #     print(f"{chars[i]}: {p1char_count[i]}")
    cur.close()
    return p1char_count

def get_p2char_count(chars, p2char_count):
    # get every player 2 character from the database
    cur = conn.cursor()
    cur.execute("SELECT player2_char FROM match_temp")
    rows = cur.fetchall()

    # updates the character count every time that character is found
    for row in rows:
        char_index = row[0]
        if char_index < len(chars):
            p2char_count[char_index] += 1
    ### Print the amount per character
    # for i in range(len(chars)):
    #     print(f"{chars[i]}: {p2char_count[i]}")
    cur.close()
    return p2char_count

def print_char_pick_rates(chars, p1char_count, p2char_count):
    # sum(p2char_count) = sum(p1char_count)
    total_games = sum(p1char_count)
    for x in range(len(chars)):
        # had to make it decimal because it wouldnt round properly
        # you can only use decimal on ints not numpy numbers, hence the cast to int
        # prints total pick rate, pick rate on player 1, pick rate on player 2
        p1_percent = Decimal(int(p1char_count[x])) / Decimal(int(total_games)) * Decimal(100)
        p2_percent = Decimal(int(p2char_count[x])) / Decimal(int(total_games)) * Decimal(100)
        total_percent = p1_percent + p2_percent
        print(f"{chars[x]}: {total_percent:.2f}% \n(P1: {p1_percent:.2f}%, P2: {p2_percent:.2f}%)")
        # prints the percentage chance that a character will be on either side if that character is picked at all
        total_chars = p1char_count[x] + p2char_count[x]
        p1_percent_char = Decimal(int(p1char_count[x])) / Decimal(int(total_chars)) * Decimal(100)
        p2_percent_char = Decimal(int(p2char_count[x])) / Decimal(int(total_chars)) * Decimal(100)
        print(f"(P1: {p1_percent_char:.2f}%, P2: {p2_percent_char:.2f}%)")

get_p1char_count(chars, p1char_count)
get_p2char_count(chars, p2char_count)
total_games = np.sum(p1char_count)

conn.close()