## Badminton Tryout System

Program created using Python, Numpy & Pygame to automate tryouts for badminton. By playing only 3 matches per player, the algorithm can rank 100+ players.

#### Learn more about the system [here](https://yiweizhou.com/projects/badminton)

Below is a user manual for the software

##### Title Page:

- Press Start to create new Teams
- Press Load to load in old teams

##### Enter Players:

- Enter player names by pressing the Enter key. Players are automatically given a number. If a player is deleted, the number is also deleted (This way if a player drops out in the middle, no numbers need to be shifted for others.)

##### Enter Match:

- The textboxes only support number entries so please enter the player number and their scores. Matches can only be entered once, if it is entered again, it will not go in the system and the corresponding message will appear.
- Required Input (Upon invalid input, the corresponding message to the user will appear):
  Valid number (player assigned)
  Valid score (less than the total points)
- The save button will save for loading. Button will appear when changes are made
- Deleting matches will delete matches from the player history and change their ranking and winnings to without the match

##### Ranking:

- Generates the ranking of all players
- By clicking on the players you can view their profile which includes their matches, wins, rank, and more
