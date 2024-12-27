Better Chess Analysis by Dat Nguyen

Project Started: 12/27/2024

This project aims to provide chess players a better experience analyzing their chess games after a match.
It's an application that will allow you to analyze your chess games by going through the different moves made throughout the match, the same way existing websites like chess.com or lichess does.
The issue with those websites, however, is that chess analysis can feel unintuitive, as they do not provide with much during analysis besides engine evaluation. You may come up with a good reason on why a move is good but you won't have anyway to write that down for future reference.  

The goal of this project is to provide a more productive way to analyze chess games and solve the issues of traditional chess analysis. The features that will be added to this app are explained below, these features will benefit the player during game analysis. Any player of any skill level will be able to use this application for their own purposes.

Features:

- Interactable Chessboard with the pieces, allowing players to make moves as you would on chess.com/lichess.
- Import Games using PGN, allowing players to import their game to analyze. PGN (Portable Game Notation) is a text file that chess.com/lichess can produce for users that provides info about the match (Players names for example) and most importantly, the notation of the moves made.
- The ability to make and save notes after each move. This allows the player to make notes on why they made that move, what their ideas were, and overall any comments about the move they made.
- The ability to make and save branches of moves. Branches are moves that you make during analysis that stem from the actual move played in game. Chess players make branches to explore alternate moves to see if there were any better moves and explore how a game would go down based off those moves. The app will allow you to save branches and provide a more convenient way to separate branches from each other.
- The ability to draw arrows and highlight squares. Drawing arrows allows players to visualize the vision of pieces or the targets/threats of a piece. Highlighting helps enhance weaknesses in a position or threats. These features are on chess.com/lichess, however this app will allow you to save arrows and highlights.
- Chess Engine Evaluation. A chess engine will be present throughout your analysis to provide feedback on moves (such as if the move was good or a blunder) and provide a value on who is better in the position (+1 if white is slightly better, -3.2 if black is significantly better). Players based off the feedback can make better notes and see better moves to improve their gameplay on future matches.
- Save Analysis. After going through the match and taking notes, drawing arrows, making branches, or highlighting, players can save their analysis in the application for later reference and start a new application.

How it works:
1. When the application starts, players will be asked to import their PGN file. Option to paste nothing if they want to start a new analysis playing against themselves.
2. Players will go through their moves they and their opponent played. Here, they can draw arrows, highlight, make notes, create move branches, to analyze their games to see how they could've improved and to see what they missed.
3. When players are done analyzing, they can save their analysis with their notes in the app, and start a new analysis or quit the application.


This project will be developed using Python 3.10