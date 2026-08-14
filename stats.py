import csv
import statistics
from collections import Counter


# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

games_file = "games_2025.csv"
players_file = "players_2025.csv"

MISSING_VALUES = {"", "NA", "N/A", "NULL", "NONE"}


# ---------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------

def is_missing(value):
    """
    Return True if a value should be treated as missing.
    """

    if value is None:
        return True

    return value.strip().upper() in MISSING_VALUES


def infer_data_type(rows, column):
    """
    Infer whether a column is numeric or non-numeric.
    """

    found_value = False

    for row in rows:

        value = row[column]

        if is_missing(value):
            continue

        found_value = True

        try:
            float(value)

        except ValueError:
            return "Non-numeric"

    if found_value:
        return "Numeric"

    return "Non-numeric"


def compute_numeric_stats(values):
    """
    Compute descriptive statistics for numeric values.
    """

    if len(values) == 0:

        return {
            "Count": 0,
            "Mean": None,
            "Minimum": None,
            "Maximum": None,
            "Standard Deviation": None,
            "Median": None
        }

    return {
        "Count": len(values),
        "Mean": statistics.mean(values),
        "Minimum": min(values),
        "Maximum": max(values),
        "Standard Deviation":
            statistics.stdev(values)
            if len(values) > 1
            else 0,
        "Median": statistics.median(values)
    }


def compute_categorical_stats(values):
    """
    Compute descriptive statistics for categorical values.
    """

    if len(values) == 0:

        return {
            "Count": 0,
            "Unique Values": 0,
            "Mode": None,
            "Mode Frequency": 0,
            "Top 5 Values": []
        }

    counts = Counter(values)

    mode, frequency = counts.most_common(1)[0]

    return {
        "Count": len(values),
        "Unique Values": len(counts),
        "Mode": mode,
        "Mode Frequency": frequency,
        "Top 5 Values": counts.most_common(5)
    }


def load_csv(filename):
    """
    Load a CSV file and return rows and column names.
    """

    with open(
        filename,
        mode="r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader = csv.DictReader(file)

        rows = list(reader)

        columns = reader.fieldnames

    return rows, columns


def analyze_dataset(rows, columns, dataset_name):
    """
    Perform descriptive statistics for a dataset.
    """

    print("\n" + "=" * 70)
    print(dataset_name)
    print("=" * 70)

    print(f"Total rows: {len(rows)}")
    print(f"Total columns: {len(columns)}")

    # -----------------------------------------------------
    # Missing Values
    # -----------------------------------------------------

    print("\nMissing Values")
    print("-" * 50)

    for column in columns:

        count = 0

        for row in rows:

            if is_missing(row[column]):
                count += 1

        print(f"{column}: {count}")

    # -----------------------------------------------------
    # Data Type Inference
    # -----------------------------------------------------

    print("\nInferred Data Types")
    print("-" * 50)

    data_types = {}

    for column in columns:

        data_types[column] = infer_data_type(
            rows,
            column
        )

        print(
            f"{column}: "
            f"{data_types[column]}"
        )

    # -----------------------------------------------------
    # Numeric Statistics
    # -----------------------------------------------------

    print("\nNumeric Column Statistics")
    print("-" * 50)

    for column in columns:

        if data_types[column] == "Numeric":

            numeric_values = []

            for row in rows:

                value = row[column]

                if is_missing(value):
                    continue

                numeric_values.append(
                    float(value)
                )

            stats = compute_numeric_stats(
                numeric_values
            )

            print(f"\nColumn: {column}")

            print(f"Count: {stats['Count']}")
            print(f"Mean: {stats['Mean']}")
            print(f"Minimum: {stats['Minimum']}")
            print(f"Maximum: {stats['Maximum']}")

            print(
                f"Standard Deviation: "
                f"{stats['Standard Deviation']}"
            )

            print(f"Median: {stats['Median']}")

    # -----------------------------------------------------
    # Categorical Statistics
    # -----------------------------------------------------

    print("\nCategorical Column Statistics")
    print("-" * 50)

    for column in columns:

        if data_types[column] == "Non-numeric":

            categorical_values = []

            for row in rows:

                value = row[column]

                if is_missing(value):
                    continue

                categorical_values.append(
                    value.strip()
                )

            stats = compute_categorical_stats(
                categorical_values
            )

            print(f"\nColumn: {column}")

            print(f"Count: {stats['Count']}")

            print(
                f"Unique Values: "
                f"{stats['Unique Values']}"
            )

            print(f"Mode: {stats['Mode']}")

            print(
                f"Mode Frequency: "
                f"{stats['Mode Frequency']}"
            )

            print("Top 5 Values:")

            for value, frequency in stats["Top 5 Values"]:

                print(
                    f"  {value}: "
                    f"{frequency}"
                )


# =========================================================
# Load Datasets
# =========================================================

games, game_columns = load_csv(
    games_file
)

players, player_columns = load_csv(
    players_file
)


# =========================================================
# Descriptive Analysis
# =========================================================

analyze_dataset(
    games,
    game_columns,
    "GAME DATASET"
)

analyze_dataset(
    players,
    player_columns,
    "PLAYER DATASET"
)


# =========================================================
# Ground-Truth Questions
# =========================================================

print("\n" + "#" * 70)
print("GROUND-TRUTH ANSWER KEY")
print("#" * 70)


# ---------------------------------------------------------
# 1. Total Games
# ---------------------------------------------------------

total_games = len(games)

print(
    f"\nTotal games played: "
    f"{total_games}"
)


# ---------------------------------------------------------
# 2. Wins and Losses
# ---------------------------------------------------------

wins = sum(
    1
    for game in games
    if game["result"] == "W"
)

losses = sum(
    1
    for game in games
    if game["result"] == "L"
)

print(f"Wins: {wins}")
print(f"Losses: {losses}")


# ---------------------------------------------------------
# 3. Total Syracuse Goals
# ---------------------------------------------------------

total_syracuse_goals = sum(
    int(game["syracuse_score"])
    for game in games
)

print(
    f"Total Syracuse goals: "
    f"{total_syracuse_goals}"
)


# ---------------------------------------------------------
# 4. Total Opponent Goals
# ---------------------------------------------------------

total_opponent_goals = sum(
    int(game["opponent_score"])
    for game in games
)

print(
    f"Total opponent goals: "
    f"{total_opponent_goals}"
)


# ---------------------------------------------------------
# 5. Average Syracuse Score
# ---------------------------------------------------------

average_syracuse_score = statistics.mean(
    int(game["syracuse_score"])
    for game in games
)

print(
    f"Average Syracuse score: "
    f"{average_syracuse_score:.2f}"
)


# ---------------------------------------------------------
# 6. Average Opponent Score
# ---------------------------------------------------------

average_opponent_score = statistics.mean(
    int(game["opponent_score"])
    for game in games
)

print(
    f"Average opponent score: "
    f"{average_opponent_score:.2f}"
)


# ---------------------------------------------------------
# 7. Average Margin of Victory
# ---------------------------------------------------------

victory_margins = []

for game in games:

    if game["result"] == "W":

        margin = (
            int(game["syracuse_score"])
            - int(game["opponent_score"])
        )

        victory_margins.append(
            margin
        )


average_margin_victory = statistics.mean(
    victory_margins
)

print(
    f"Average margin of victory: "
    f"{average_margin_victory:.2f}"
)


# ---------------------------------------------------------
# 8. Highest Combined-Scoring Game
# ---------------------------------------------------------

highest_combined_game = max(
    games,
    key=lambda game:
        int(game["syracuse_score"])
        + int(game["opponent_score"])
)

highest_combined_score = (
    int(
        highest_combined_game["syracuse_score"]
    )
    +
    int(
        highest_combined_game["opponent_score"]
    )
)

print(
    "\nHighest combined-scoring game:"
)

print(
    f"{highest_combined_game['opponent']} "
    f"({highest_combined_game['syracuse_score']}-"
    f"{highest_combined_game['opponent_score']})"
)

print(
    f"Combined score: "
    f"{highest_combined_score}"
)


# ---------------------------------------------------------
# 9. Most Goals by a Player
# ---------------------------------------------------------

top_goal_scorer = max(
    players,
    key=lambda player:
        int(player["goals"])
)

print(
    "\nTop goal scorer:"
)

print(
    f"{top_goal_scorer['player']} - "
    f"{top_goal_scorer['goals']} goals"
)


# ---------------------------------------------------------
# 10. Most Assists
# ---------------------------------------------------------

top_assist_player = max(
    players,
    key=lambda player:
        int(player["assists"])
)

print(
    "\nAssist leader:"
)

print(
    f"{top_assist_player['player']} - "
    f"{top_assist_player['assists']} assists"
)


# ---------------------------------------------------------
# 11. Most Points
# ---------------------------------------------------------

top_points_player = max(
    players,
    key=lambda player:
        int(player["points"])
)

print(
    "\nPoints leader:"
)

print(
    f"{top_points_player['player']} - "
    f"{top_points_player['points']} points"
)


# ---------------------------------------------------------
# 12. Most Ground Balls
# ---------------------------------------------------------

top_ground_balls = max(
    players,
    key=lambda player:
        int(player["ground_balls"])
)

print(
    "\nGround ball leader:"
)

print(
    f"{top_ground_balls['player']} - "
    f"{top_ground_balls['ground_balls']} ground balls"
)


# ---------------------------------------------------------
# 13. Most Draw Controls
# ---------------------------------------------------------

top_draw_controls = max(
    players,
    key=lambda player:
        int(player["draw_controls"])
)

print(
    "\nDraw control leader:"
)

print(
    f"{top_draw_controls['player']} - "
    f"{top_draw_controls['draw_controls']} draw controls"
)


# ---------------------------------------------------------
# 14. Most Caused Turnovers
# ---------------------------------------------------------

top_caused_turnovers = max(
    players,
    key=lambda player:
        int(player["caused_turnovers"])
)

print(
    "\nCaused turnover leader:"
)

print(
    f"{top_caused_turnovers['player']} - "
    f"{top_caused_turnovers['caused_turnovers']} "
    f"caused turnovers"
)


print(
    "\nGround-truth analysis completed successfully."
)


# ---------------------------------------------------------
# Phase B - Offensive Impact Score
# ---------------------------------------------------------

print("\n" + "#" * 70)
print("PHASE B - QUALITATIVE METRIC")
print("#" * 70)

impact_scores = []

for player in players:

    goals = int(player["goals"])
    assists = int(player["assists"])
    game_winners = int(player["game_winners"])

    impact_score = (
        goals
        + assists
        + (2 * game_winners)
    )

    impact_scores.append(
        (player["player"], impact_score)
    )


impact_scores.sort(
    key=lambda x: x[1],
    reverse=True
)


print("\nTop 5 Offensive Impact Scores:")

for player, score in impact_scores[:5]:
    print(f"{player}: {score}")


most_impactful = impact_scores[0]

print(
    f"\nMost Impactful Offensive Player: "
    f"{most_impactful[0]}"
)

print(
    f"Offensive Impact Score: "
    f"{most_impactful[1]}"
)

# ---------------------------------------------------------
# Phase B - MVP Score
# ---------------------------------------------------------

mvp_scores = []

for player in players:

    points = int(player["points"])
    game_winners = int(player["game_winners"])
    ground_balls = int(player["ground_balls"])
    draw_controls = int(player["draw_controls"])
    caused_turnovers = int(player["caused_turnovers"])
    turnovers = int(player["turnovers"])

    mvp_score = (
        points
        + (2 * game_winners)
        + ground_balls
        + draw_controls
        + caused_turnovers
        - turnovers
    )

    mvp_scores.append(
        (player["player"], mvp_score)
    )


mvp_scores.sort(
    key=lambda x: x[1],
    reverse=True
)


print("\nTop 5 MVP Scores:")

for player, score in mvp_scores[:5]:
    print(f"{player}: {score}")


mvp = mvp_scores[0]

print(
    f"\nHighest MVP Score: "
    f"{mvp[0]} - {mvp[1]}"
)
