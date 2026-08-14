# Task 05: Descriptive Statistics and Large Language Models

## Project Description

This project investigates how reliably a Large Language Model (LLM) can answer descriptive-statistics questions when provided with a small real-world dataset.

The experiment uses statistics from the **2025 Syracuse University Women's Lacrosse season**. Ground-truth answers were first calculated programmatically using Python. The same questions were then given to an LLM, and its responses were compared against the verified results.

The experiment was completed in two phases:

- **Phase A:** Baseline factual and numerical questions
- **Phase B:** More complex questions, qualitative metrics, advisory analysis, and prompt engineering

The purpose of the project is not only to determine whether an LLM can produce correct answers, but also to examine the types of errors it makes and whether better prompting can improve its analytical reliability.

---

# Dataset

The project uses data from the **2025 Syracuse University Women's Lacrosse season**.

The original statistics were obtained from the official Syracuse Athletics season statistics.

The data was organized into two small CSV files for analysis.

## `games_2025.csv`

This file contains game-level information including:

- Date
- Opponent
- Win/loss result
- Syracuse score
- Opponent score
- Attendance

The dataset contains **19 games**.

## `players_2025.csv`

This file contains cumulative player statistics including:

- Player name
- Games played
- Goals
- Assists
- Points
- Shots
- Game-winning goals
- Ground balls
- Draw controls
- Turnovers
- Caused turnovers
- Fouls

Summary rows such as team totals and opponent totals were excluded so that player-level descriptive statistics would not be distorted.

---

# Ground Truth

Before asking the LLM any questions, a Python script was used to establish programmatically verified ground-truth statistics.

The script is:

`ground_truth_stats.py`

The script calculates descriptive statistics for both datasets and produces an answer key for the questions used during the experiment.

Some of the verified season-level results were:

- Games played: **19**
- Record: **10-9**
- Total Syracuse goals: **235**
- Total opponent goals: **221**
- Average Syracuse goals per game: **12.37**
- Average opponent goals per game: **11.63**
- Average margin of victory: **5.50 goals**
- Highest combined-scoring game: **Syracuse vs. UAlbany, 21-9, 30 combined goals**
- Goal leader: **Emma Muchnick — 34 goals**
- Assist leader: **Emma Ward — 46 assists**
- Points leader: **Emma Ward — 76 points**
- Draw-control leader: **Meghan Rode — 75**
- Caused-turnover leader: **Coco Vandiver — 40**

These programmatically calculated values were used to evaluate the LLM responses.

---

# Running the Ground-Truth Analysis

Python 3 is required.

Place the CSV files and Python script in the same directory:

```text
Task_05_Descriptive_Stats/
│
├── README.md
├── PROMPT_LOG.md
├── ground_truth_stats.py
├── games_2025.csv
└── players_2025.csv
```

Run the ground-truth analysis using:

```bash
python ground_truth_stats.py
```

The script uses only Python standard-library modules:

```text
csv
statistics
collections
```

Therefore, no third-party Python libraries are required.

---

# Phase A — Baseline Factual Questions

Phase A tested whether the LLM could answer relatively straightforward factual and numerical questions using the provided datasets.

Ten questions were asked, beginning with simple lookups and progressing to calculations and aggregations.

The questions included:

1. How many games did Syracuse Women's Lacrosse play in the 2025 season?
2. What was Syracuse Women's Lacrosse's overall win-loss record?
3. How many total goals did Syracuse Women's Lacrosse score?
4. Which player scored the most goals?
5. Which player recorded the most assists?
6. Which player had the most total points?
7. What was Syracuse's average number of goals scored per game?
8. What was Syracuse's average margin of victory?
9. Which game had the highest combined score?
10. Which player recorded the most draw controls?

The complete prompts, responses, ground-truth answers, and evaluations are documented in `PROMPT_LOG.md`.

---

# Phase A Findings

The LLM performed well on many questions that involved directly identifying a maximum value or retrieving information from the player dataset.

For example, it correctly identified:

- **Emma Muchnick** as the goal leader with 34 goals
- **Emma Ward** as the assist leader with 46 assists
- **Emma Ward** as the points leader with 76 points
- **Meghan Rode** as the draw-control leader with 75
- **Syracuse vs. UAlbany** as the highest combined-scoring game with 30 total goals

However, several numerical errors occurred.

One of the clearest examples involved Syracuse's season record. The ground truth was **10 wins and 9 losses**, but the model initially reported **9 wins and 10 losses**.

Another error occurred when calculating total goals. The model reported **231 goals**, while the programmatically verified total was **235 goals**.

This incorrect total then affected a later calculation. The model used:

```text
231 / 19 = 12.16
```

and therefore reported an average of **12.16 goals per game**.

The correct calculation was:

```text
235 / 19 = 12.37
```

This demonstrated that an incorrect intermediate result can propagate into later responses.

Another notable error occurred when calculating average margin of victory. The model correctly identified the 10 winning games and correctly calculated their individual victory margins. It also correctly summed those margins to 55. However, it then divided by 9 instead of 10 and reported an incorrect final result.

The correct calculation was:

```text
55 / 10 = 5.50
```

These examples show that an LLM may correctly retrieve data and even perform several intermediate steps correctly while still producing an incorrect final answer.

---

# Phase B — Qualitative Metrics and Prompt Engineering

Phase B explored questions that did not necessarily have a single predefined answer.

Instead of asking only factual questions, qualitative concepts were explicitly defined using mathematical formulas so that reproducible ground truth could be established.

---

## Offensive Impact Score

The first qualitative metric was **Most Impactful Offensive Player**.

For this experiment, the metric was defined as:

```text
Offensive Impact Score =
Goals + Assists + (2 × Game-Winning Goals)
```

The Python ground-truth calculation identified:

**Emma Ward — Offensive Impact Score: 78**

Her calculation was:

```text
30 + 46 + (2 × 1) = 78
```

When the same definition was provided to the LLM, it correctly identified Emma Ward and correctly calculated the score of 78.

This suggested that explicitly defining an otherwise subjective concept can make the LLM's answer more consistent and reproducible.

---

# Vague vs. Explicit Questions

The LLM was also asked a more subjective question:

> Based on the 2025 Syracuse Women's Lacrosse player data, who was the most valuable player on the team? Explain your reasoning using the data.

Without an explicit definition of "most valuable," the model selected **Emma Ward**.

The model chose its own criteria and emphasized her total points, assists, goals, full-season participation, and offensive contribution.

The answer was reasonable, but it could not be considered objectively correct because the term **most valuable** had not been mathematically defined.

The experiment therefore introduced an explicit MVP metric.

---

# MVP Score

For this experiment, MVP was defined as:

```text
MVP Score =
Points
+ (2 × Game-Winning Goals)
+ Ground Balls
+ Draw Controls
+ Caused Turnovers
- Turnovers
```

This metric attempts to include offensive production, possession, defensive contribution, important goals, and the negative effect of turnovers.

The Python ground-truth Top 5 was:

```text
1. Joely Caramelli — 85
2. Meghan Rode — 73
3. Coco Vandiver — 72
4. Alexa Vogelman — 69
5. Emma Muchnick — 63
```

The LLM correctly identified **Joely Caramelli** as the MVP with a score of **85**.

The calculation was:

```text
20 + (2 × 0) + 23 + 39 + 11 - 8 = 85
```

However, its Top 5 ranking was incorrect.

An interesting finding was that the model correctly calculated Meghan Rode's score as 73 and Coco Vandiver's score as 72 earlier in its response, but then omitted both players from its final Top 5 ranking.

This was a ranking and sorting error rather than an error in applying the MVP formula.

---

# Prompt Engineering Experiment

A follow-up prompt explicitly instructed the model to calculate all scores, sort them numerically from highest to lowest, and only then select the Top 5.

The stronger prompt improved the result because **Meghan Rode** was correctly included.

However, **Coco Vandiver**, whose calculated score was 72, was still incorrectly excluded from the Top 5 even though the model had calculated her score correctly.

The correct ranking remained:

```text
1. Joely Caramelli — 85
2. Meghan Rode — 73
3. Coco Vandiver — 72
4. Alexa Vogelman — 69
5. Emma Muchnick — 63
```

This demonstrated that more explicit instructions can improve LLM performance without necessarily eliminating all errors.

---

# Advisory Analysis

The final part of Phase B asked the LLM to move beyond descriptive statistics and make a recommendation based on the data.

The model was asked whether Syracuse should focus more on improving offense or defense if the goal was to win at least two additional games in the following season. It was also asked to identify one player who could potentially be a game changer.

In its initial response, the model recommended focusing on **defense** and selected **Alexa Vogelman**.

The recommendation itself was plausible, but several supporting statistics were incorrect.

The response used:

- 231 goals instead of 235
- 211 opponent goals instead of 221
- A 9-10 record instead of 10-9
- 12.16 goals per game instead of 12.37
- 11.11 opponent goals per game instead of 11.63
- 6.11 average victory margin instead of 5.50

This showed an important problem: a convincing analytical narrative can still be based on incorrect numerical evidence.

---

# Improved Advisory Prompt

A stronger follow-up prompt instructed the model to:

1. Ignore previous calculations and conclusions.
2. Recalculate statistics directly from the uploaded CSV files.
3. Verify the core statistics before making a recommendation.
4. Clearly distinguish facts from interpretations.
5. Avoid predictions that could not be supported by the provided data.

The response improved substantially.

The model correctly recalculated:

- Record: **10-9**
- Goals scored: **235**
- Goals allowed: **221**
- Goal differential: **+14**
- Average goals scored: **12.37**
- Average goals allowed: **11.63**
- Average victory margin: **5.50**
- Average loss margin: **4.56**

It again recommended prioritizing **defense**, but this time selected **Coco Vandiver** as the potential game-changing player.

The recommendation was supported by statistics including:

- **40 caused turnovers**
- **34 ground balls**
- **19 games played**
- **51 fouls**

The model also appropriately identified Vandiver's high foul count as a possible limitation.

However, the improved response still contained smaller counting errors.

The model stated that six of Syracuse's 10 wins were decided by two goals or fewer. The correct number was **four**.

It also stated that six of Syracuse's nine losses were decided by three goals or fewer. The correct number was **five**.

Therefore, prompt engineering substantially improved the response but did not completely eliminate numerical errors.

---

# Overall Findings

The experiment showed that LLMs can be useful for exploring and interpreting small datasets, but their numerical outputs should not automatically be treated as ground truth.

The LLM performed particularly well when:

- Retrieving individual player statistics
- Identifying maximum values
- Applying clearly defined formulas
- Explaining statistical results in natural language
- Producing interpretations from verified statistics

The model was less reliable when:

- Counting categories
- Summing many values
- Performing multi-step arithmetic
- Ranking a large set of calculated values
- Carrying calculations across multiple questions
- Producing advisory conclusions without first verifying numerical evidence

One particularly important observation was **error propagation**. An incorrect total from an earlier question was reused in later calculations, causing additional incorrect answers.

Another important observation was that correct intermediate calculations did not guarantee a correct final result. The model sometimes calculated individual values correctly but made mistakes when sorting, ranking, counting, or summarizing them.

---

# Prompt Engineering Findings

Prompt engineering noticeably improved the reliability of the model's analysis.

Prompts were more effective when they:

- Explicitly defined qualitative metrics
- Required the model to recalculate values from the original CSV files
- Asked the model not to rely on previous responses
- Required intermediate calculations
- Required numerical sorting before ranking
- Asked the model to distinguish facts from interpretations
- Asked the model to avoid unsupported predictions

However, prompt engineering did not guarantee perfect numerical accuracy.

For example, even after being explicitly instructed to sort all MVP scores numerically, the model still omitted a player whose calculated score should have placed her in the Top 5.

Similarly, the improved coaching prompt corrected the major season-level statistics but still produced smaller counting errors.

This suggests that prompt engineering can reduce errors but does not replace independent verification.

---

# Reflection

The experiment changed how I view the role of LLMs in descriptive data analysis.

An LLM can be useful for explaining data, generating possible interpretations, and helping formulate analytical questions. It can also correctly perform many straightforward lookups and calculations.

However, it should not replace a reproducible statistical program when numerical accuracy is important.

The ground-truth Python script was essential because it provided an independent answer key against which every LLM response could be checked.

One of the most interesting observations was that the model could produce responses that appeared detailed and convincing while containing incorrect calculations. In several cases, the model showed correct intermediate values but still produced an incorrect final answer.

The experiment also demonstrated the importance of conversational context. Some incorrect calculations from earlier prompts were reused in later responses. Asking the model to ignore previous calculations and recompute statistics directly from the original files substantially improved its accuracy.

Prompt engineering therefore improved the quality of the responses, especially when the model was asked to verify values before interpreting them.

At the same time, prompt engineering did not completely eliminate errors. Even after receiving explicit instructions, the model occasionally made mistakes in ranking, sorting, or counting.

The most effective workflow therefore appears to combine traditional programming with LLM assistance:

```text
Dataset
   ↓
Programmatic Ground Truth
   ↓
LLM Analysis
   ↓
Verification Against Ground Truth
   ↓
Interpretation
```

Python provides reproducibility and numerical verification, while the LLM is more useful for explanation, exploration, and interpretation.

The main lesson from this experiment is that a confident and well-written LLM response is not necessarily a correct one. Numerical claims should still be independently verified before they are used to support conclusions or decisions.

---

# Prompt and Response Log

The complete record of the experiment is available in:

**`PROMPT_LOG.md`**

The log contains:

- Model and version used
- Exact prompts
- Complete model responses
- Programmatically calculated ground truth
- Verdicts
- Notes explaining errors and observations

---

# Repository Structure

```text
Task_05_Descriptive_Stats/
│
├── README.md
├── PROMPT_LOG.md
├── ground_truth_stats.py
├── games_2025.csv
└── players_2025.csv
```

---

# Dataset Source

The original data was obtained from the official **Syracuse University Athletics 2025 Women's Lacrosse season statistics**.

The original Syracuse Athletics statistics were used as the source for creating the smaller game-level and player-level datasets used in this experiment.

The source data should be obtained from the official Syracuse Athletics source rather than redistributed through this repository.
