import argparse
from collections import defaultdict

def parse_input(input_lines):
    """
    Parses input lines into a list of games, each containing two teams and their respective scores.
    
    Args:
        input_lines (list of str): A list of strings where each string is a line representing a game result
                                   in the format "Team1 Score1, Team2 Score2".

    Returns:
        list of tuples: A list of tuples, each containing (team1_name, team1_score, team2_name, team2_score).
    """
    games = []
    for line in input_lines:
        if line.strip():  # Only process non-empty lines
            team1, score1, team2, score2 = parse_line(line)
            games.append((team1, score1, team2, score2))
    return games

def parse_line(line):
    """
    Parses a single line of input to extract team names and scores, ensuring scores are non-negative.
    
    Args:
        line (str): A single line of text in the format "Team1 Score1, Team2 Score2".

    Returns:
        tuple: A tuple containing (team1_name, team1_score, team2_name, team2_score).
    
    Raises:
        ValueError: If either score is negative.
    """
    parts = line.split(',')
    team1_name, team1_score = parts[0].strip().rsplit(' ', 1)
    team2_name, team2_score = parts[1].strip().rsplit(' ', 1)

    team1_score = int(team1_score)
    team2_score = int(team2_score)

    # Check for negative scores
    if team1_score < 0 or team2_score < 0:
        raise ValueError("Scores must be non-negative")

    return team1_name.strip(), team1_score, team2_name.strip(), team2_score


def calculate_scores(games):
    """
    Calculates scores for each team based on a list of game results.
    
    Args:
        games (list of tuples): A list where each tuple represents a game and contains
                                (team1_name, team1_score, team2_name, team2_score).

    Returns:
        dict: A dictionary where keys are team names and values are their accumulated points.
    """
    scores = defaultdict(int)
    
    for team1, score1, team2, score2 in games:
        scores.setdefault(team1, 0)
        scores.setdefault(team2, 0)
        
        if score1 > score2:
            scores[team1] += 3
        elif score1 < score2:
            scores[team2] += 3
        else:
            scores[team1] += 1
            scores[team2] += 1
    
    return scores

def format_ranked_teams(scores):
    """
    Formats the ranked teams and scores according to the original expected output format.
    
    Args:
        scores (dict): A dictionary of team names and their accumulated points.

    Returns:
        list of str: A list of formatted strings representing the ranked teams with their scores.
                     Teams with the same rank share the same position in the output.
    """
    sorted_teams = sorted(scores.items(), key=lambda x: (-x[1], x[0]))
    output = []
    last_points = None
    rank = 0
    current_position = 0

    for team, points in sorted_teams:
        current_position += 1
        if points != last_points:
            rank = current_position
        points_label = "pt" if points == 1 else "pts"
        output.append(f"{rank}. {team}, {points} {points_label}")
        last_points = points
    
    return output

def main(input_file):
    """
    Main function to execute the league ranking process.
    
    Args:
        input_file (str): The path to the file containing the list of game results.
    """
    with open(input_file, 'r') as file:
        input_lines = file.readlines()

    games = parse_input(input_lines)
    scores = calculate_scores(games)
    ranked_teams = format_ranked_teams(scores)

    print("\n".join(ranked_teams))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate league rankings based on game results.")
    parser.add_argument("input_file", help="Path to the input file containing game results.")
    args = parser.parse_args()
    
    main(args.input_file)
