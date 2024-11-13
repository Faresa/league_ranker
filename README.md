# League Ranker

## Overview

League Ranker is a Python program that ranks teams based on game results. It parses game scores, calculates points, and displays rankings in a readable format.

## Features

- Parses team names and scores from game results
- Calculates points for wins, losses, and draws
- Outputs a ranked list of teams based on points

## Getting Started

### Prerequisites

- **Python 3.11+**
- **pytest** (for running tests)

### Installing `pip` and `pipenv`

1. **Install `pip**:
   
   If not already installed, install `pip` by running:

   ```bash
   sudo apt update
   sudo apt install python3-pip
   ```

2. **Install `pipenv`** (recommended for managing dependencies):

   ```bash
   pip install pipenv
   ```

3. **Install `pytest`**:

   ```bash
   pip install pytest
   ```

### Setup

1. **Clone the Repository**:

    ```bash
    git clone <repository_url>
    cd league_ranker
    ```

2. **Set up a Virtual Environment with `pipenv`** (recommended):

    ```bash
    pipenv install --dev
    pipenv shell
    ```

   Or, if using a standard virtual environment:

    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

## Usage

1. Create an input file with game results in the format:
   
    ```
    Team1 Score1, Team2 Score2
    ```

   Example input file content:

    ```
    Mighty Eagles 3, Thunder Wolves 2
    Coastal Bears 1, Golden Sharks 1
    Mighty Eagles 2, Golden Sharks 1
    Thunder Wolves 0, Coastal Bears 3
    Mighty Eagles 1, Coastal Bears 2
    ```

2. Run the program with:

    ```bash
    python league_ranker.py <input_file>
    ```

Example output:

```
1. Coastal Bears, 7 pts
2. Mighty Eagles, 6 pts
3. Golden Sharks, 1 pt
4. Thunder Wolves, 0 pts
```

## Testing

Tests are in `test_league_ranker.py` and cover basic functionality and edge cases.

Run all tests with:

```bash
pytest test_league_ranker.py
```

## License

MIT License
