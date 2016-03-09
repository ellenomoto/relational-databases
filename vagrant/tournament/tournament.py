#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager
"""added context manager per recommendation of past Udacity reviewer"""

@contextmanager
def cursor():
    """Helper function to connect and closer cursors using context manager for queries.
    """
    conn = connect()
    cur = conn.cursor()
    try:
        yield cur
    except:
        print ("Failed to yield cursor.")
    conn.commit()
    cur.close()
    conn.close()

def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        """added try block per recommendation of past Udacity reviewer
        it is noted that in a more complex program specific exceptions 
        should be caught"""
        print ("Failed to connect to database: tournament.")


def deleteMatches():
    """Remove all the match records from the database."""
    with cursor() as c:
        c.execute("DELETE from Match;")


def deletePlayers():
    """Remove all the player records from the database."""
    with cursor() as c:
        c.execute("DELETE from Player;")


def countPlayers():
    """Returns the number of players currently registered."""
    with cursor() as c:
        c.execute("SELECT COUNT(*) from Player;")
        playerCount = c.fetchone()[0]
    return playerCount

def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    x = name
    with cursor() as c:
        c.execute("INSERT INTO Player (name, wins, losses, ties) VALUES (%s, %s, %s, %s);", (name, 0, 0, 0))


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    playerStandings = []
    with cursor() as c:
        c.execute("SELECT * from Player;")
        for player in c:
            playerStandings.append((player[0], player[1], player[2], player[2]+player[3]+player[4]))
    return sorted(playerStandings, key=lambda x: x[2])


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with cursor() as c:
        c.execute("INSERT INTO Match (winner, loser) VALUES (%s, %s);", (winner, loser))
        c.execute("UPDATE Player SET wins = wins+1 WHERE id=%s;", (winner,))
        c.execute("UPDATE Player SET losses = losses+1 WHERE id=%s;", (loser,))
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    playerRankings = playerStandings()
    swissPairs = []
    for index in range(len(playerRankings)/2):
        player1 = playerRankings[index*2]
        player2 = playerRankings[(index*2)+1]
        swissPairs.append((player1[0], player1[1], player2[0], player2[1]))
    return swissPairs


