import pytest
from league_ranker import parse_line, parse_input, calculate_scores, format_ranked_teams

def test_parse_line():
    """
    Test parse_line to ensure it correctly extracts team names and scores.
    
    Scenarios:
    - Basic input format (e.g., "Lions 3, Snakes 2")
    - Extra spaces around team names and scores
    - Draw (same score for both teams)
    """
    # Basic valid input
    line = "Lions 3, Snakes 2"
    result = parse_line(line)
    assert result == ("Lions", 3, "Snakes", 2)

    # Input with extra spaces
    line = "   Lions   3 , Snakes  2  "
    result = parse_line(line)
    assert result == ("Lions", 3, "Snakes", 2)

    # Input where both teams score the same (draw)
    line = "Tarantulas 1, FC Awesome 1"
    result = parse_line(line)
    assert result == ("Tarantulas", 1, "FC Awesome", 1)

def test_parse_input():
    """
    Test parse_input to confirm it parses multiple lines of game results.
    
    Verifies that each line is correctly passed through parse_line and
    returns a list of tuples representing games.
    """
    lines = [
        "Lions 3, Snakes 3",
        "Tarantulas 1, FC Awesome 0",
        "Lions 1, FC Awesome 1"
    ]
    result = parse_input(lines)
    expected = [
        ("Lions", 3, "Snakes", 3),
        ("Tarantulas", 1, "FC Awesome", 0),
        ("Lions", 1, "FC Awesome", 1)
    ]
    assert result == expected

def test_calculate_scores():
    """
    Test calculate_scores to ensure it correctly accumulates points based on game results.
    
    Scenarios:
    - Winning team receives 3 points
    - Draw results in 1 point for each team
    - Points accumulate across multiple games
    """
    games = [
        ("Lions", 3, "Snakes", 3),      # Draw, 1 point each
        ("Tarantulas", 1, "FC Awesome", 0),  # Tarantulas win, 3 points
        ("Lions", 1, "FC Awesome", 1),  # Draw, 1 point each
        ("Snakes", 2, "Lions", 1)       # Snakes win, 3 points
    ]
    result = calculate_scores(games)
    expected = {
        "Lions": 2,
        "Snakes": 4,
        "Tarantulas": 3,
        "FC Awesome": 1
    }
    assert result == expected

def test_format_ranked_teams():
    """
    Test format_ranked_teams to verify it correctly sorts and formats the ranking output.
    
    Scenarios:
    - Teams are sorted by points (highest to lowest)
    - Alphabetical order for teams with tied points
    - Correct formatting with singular 'pt' and plural 'pts' based on points
    """
    scores = {
        "Lions": 5,
        "Tarantulas": 6,
        "FC Awesome": 1,
        "Snakes": 1,
        "Grouches": 0
    }
    result = format_ranked_teams(scores)
    expected = [
        "1. Tarantulas, 6 pts",
        "2. Lions, 5 pts",
        "3. FC Awesome, 1 pt",
        "3. Snakes, 1 pt",
        "5. Grouches, 0 pts"
    ]
    assert result == expected

def test_parse_line_edge_cases():
    """
    Test parse_line with various edge cases for input handling.
    
    Scenarios:
    - Extra spaces between scores and team names
    - Large scores for teams
    - Team names with multiple words
    - Score of zero for one team
    - Handling invalid input cases (no scores or missing team names)
    """
    # Extra spaces between scores and team names
    line = "   Lions    10 ,   Snakes   5   "
    result = parse_line(line)
    assert result == ("Lions", 10, "Snakes", 5)

    # Large scores
    line = "Dragons 9999, Phoenix 8888"
    result = parse_line(line)
    assert result == ("Dragons", 9999, "Phoenix", 8888)

    # Team names with multiple words
    line = "The Mighty Ducks 3, Los Angeles Dragons 2"
    result = parse_line(line)
    assert result == ("The Mighty Ducks", 3, "Los Angeles Dragons", 2)

    # Score of zero for one team
    line = "Lions 0, Snakes 5"
    result = parse_line(line)
    assert result == ("Lions", 0, "Snakes", 5)

    # Handling invalid input (no scores)
    line = "Lions , Snakes"
    with pytest.raises(ValueError):
        parse_line(line)

    # Handling missing team names
    line = "3, 2"
    with pytest.raises(ValueError):
        parse_line(line)

def test_parse_input_empty_lines():
    """
    Test parse_input with empty lines and additional whitespace.
    
    Verifies that empty or whitespace-only lines are ignored and 
    does not affect the parsed output.
    """
    lines = [
        "Lions 3, Snakes 3",
        "   ",               # Empty line with spaces
        "\t",                # Empty line with tab
        "Tarantulas 1, FC Awesome 0"
    ]
    result = parse_input(lines)
    expected = [
        ("Lions", 3, "Snakes", 3),
        ("Tarantulas", 1, "FC Awesome", 0)
    ]
    assert result == expected

def test_calculate_scores_duplicates_and_extreme_cases():
    """
    Test calculate_scores with duplicate games, high scores, and unusual patterns.
    
    Scenarios:
    - Draws with multiple occurrences (duplicates)
    - Games with extremely high scores
    - Different outcomes between the same teams
    """
    games = [
        ("Lions", 5, "Snakes", 5),  # Draw, 1 point each
        ("Tarantulas", 20, "FC Awesome", 0),  # Tarantulas win, extreme score
        ("Lions", 2, "Snakes", 2),  # Another draw
        ("Lions", 5, "Snakes", 5),  # Duplicate draw (should still count)
        ("Snakes", 3, "Lions", 0)   # Snakes win, same teams different outcome
    ]
    result = calculate_scores(games)
    expected = {
        "Lions": 3,        # 1 (first draw) + 1 (second draw) + 1 (duplicate draw)
        "Snakes": 6,       # 1 + 1 + 1 + 3
        "Tarantulas": 3,   # 3 points from win
        "FC Awesome": 0    # 0 points from loss
    }
    assert result == expected

def test_format_ranked_teams_ties_and_single_point():
    """
    Test format_ranked_teams with multiple ties and different ranking scenarios.
    
    Scenarios:
    - Multiple teams with the same points
    - Correct ordering and formatting for single and plural points
    """
    scores = {
        "Lions": 3,
        "Snakes": 3,
        "Tarantulas": 1,
        "FC Awesome": 1,
        "Dragons": 1
    }
    result = format_ranked_teams(scores)
    expected = [
        "1. Lions, 3 pts",
        "1. Snakes, 3 pts",
        "3. Dragons, 1 pt",
        "3. FC Awesome, 1 pt",
        "3. Tarantulas, 1 pt"
    ]
    assert result == expected

def test_format_ranked_teams_large_points():
    """
    Test format_ranked_teams with large point differences to ensure ranking is consistent.
    
    Scenarios:
    - Teams with significantly high scores
    - Confirm proper ranking and formatting with large numbers
    """
    scores = {
        "Dragons": 1000,
        "Lions": 500,
        "Phoenix": 500,
        "Snakes": 10,
        "Tarantulas": 5
    }
    result = format_ranked_teams(scores)
    expected = [
        "1. Dragons, 1000 pts",
        "2. Lions, 500 pts",
        "2. Phoenix, 500 pts",
        "4. Snakes, 10 pts",
        "5. Tarantulas, 5 pts"
    ]
    assert result == expected

def test_parse_line_negative_score():
    """
    Test parse_line raises ValueError for negative scores.
    """
    line = "Lions -1, Snakes 3"
    with pytest.raises(ValueError, match="Scores must be non-negative"):
        parse_line(line)

    line = "Lions 2, Snakes -5"
    with pytest.raises(ValueError, match="Scores must be non-negative"):
        parse_line(line)