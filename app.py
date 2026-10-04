import streamlit as st
import random
import time

from solver import solve_puzzle


# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="AI Puzzle Solver",
    page_icon="🧩",
    layout="centered"
)


# ==========================================
# GOAL STATE
# ==========================================

GOAL = (
    1, 2, 3,
    4, 5, 6,
    7, 8, 0
)


# ==========================================
# TITLE
# ==========================================

st.title("🧩 AI Puzzle Solver")

st.write(
    "An intelligent 8-Puzzle solver using "
    "A* Search and Manhattan Distance."
)

st.divider()


# ==========================================
# AI INFORMATION
# ==========================================

st.subheader("🤖 AI Engine")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🔍 **Algorithm**\n\nA* Search")

with col2:
    st.info("📐 **Heuristic**\n\nManhattan Distance")

with col3:
    st.info("🧠 **Formula**\n\nf(n) = g(n) + h(n)")


# ==========================================
# SESSION STATE
# ==========================================

if "puzzle" not in st.session_state:

    st.session_state.puzzle = [
        1, 2, 3,
        4, 0, 6,
        7, 5, 8
    ]


# ==========================================
# RANDOM PUZZLE GENERATOR
# ==========================================

def generate_puzzle(difficulty):

    puzzle = list(GOAL)

    if difficulty == "Easy":
        moves = 10

    elif difficulty == "Medium":
        moves = 30

    else:
        moves = 60

    previous_zero = -1

    for _ in range(moves):

        zero_index = puzzle.index(0)

        row = zero_index // 3
        col = zero_index % 3

        possible_moves = []

        if row > 0:
            possible_moves.append(zero_index - 3)

        if row < 2:
            possible_moves.append(zero_index + 3)

        if col > 0:
            possible_moves.append(zero_index - 1)

        if col < 2:
            possible_moves.append(zero_index + 1)

        if (
            previous_zero in possible_moves
            and len(possible_moves) > 1
        ):
            possible_moves.remove(previous_zero)

        new_zero = random.choice(possible_moves)

        puzzle[zero_index], puzzle[new_zero] = (
            puzzle[new_zero],
            puzzle[zero_index]
        )

        previous_zero = zero_index

    return puzzle


# ==========================================
# DIFFICULTY
# ==========================================

st.subheader("🎯 Puzzle Difficulty")

difficulty = st.selectbox(
    "Select difficulty:",
    ["Easy", "Medium", "Hard"]
)


# ==========================================
# GENERATE PUZZLE
# ==========================================

if st.button(
    "🎲 Generate New Puzzle",
    use_container_width=True
):

    st.session_state.puzzle = generate_puzzle(
        difficulty
    )

    st.rerun()


# ==========================================
# MOVE TILE
# ==========================================

def move_tile(index):

    puzzle = st.session_state.puzzle

    zero_index = puzzle.index(0)

    row1 = index // 3
    col1 = index % 3

    row2 = zero_index // 3
    col2 = zero_index % 3

    if abs(row1 - row2) + abs(col1 - col2) == 1:

        puzzle[index], puzzle[zero_index] = (
            puzzle[zero_index],
            puzzle[index]
        )

        st.session_state.puzzle = puzzle


# ==========================================
# DISPLAY PUZZLE
# ==========================================

st.divider()

st.subheader("🎮 Puzzle Board")

st.write(
    "Click a tile next to the empty space to move it."
)

puzzle = st.session_state.puzzle


for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        index = row * 3 + col

        value = puzzle[index]

        with cols[col]:

            if value == 0:

                st.button(
                    "⬜",
                    key=f"tile_{index}",
                    use_container_width=True
                )

            else:

                if st.button(
                    str(value),
                    key=f"tile_{index}",
                    use_container_width=True
                ):

                    move_tile(index)


# ==========================================
# CURRENT PUZZLE
# ==========================================

st.subheader("📌 Current State")

st.code(
    f"""
{puzzle[0]} | {puzzle[1]} | {puzzle[2]}
-----------
{puzzle[3]} | {puzzle[4]} | {puzzle[5]}
-----------
{puzzle[6]} | {puzzle[7]} | {puzzle[8]}
"""
)


# ==========================================
# SOLVE WITH AI + ANIMATION
# ==========================================

st.divider()

if st.button(
    "🧠 Solve & Animate",
    use_container_width=True
):

    start = tuple(st.session_state.puzzle)

    if start == GOAL:

        st.success(
            "🎉 Puzzle is already solved!"
        )

    else:

        with st.spinner(
            "🤖 A* AI is finding the solution..."
        ):

            solution = solve_puzzle(
                start,
                GOAL
            )

        if solution is None:

            st.error(
                "❌ No solution found."
            )

        else:

            st.success(
                f"🎉 Solution found in {len(solution)} moves!"
            )

            st.subheader(
                "🤖 AI Solving..."
            )

            # ----------------------------------
            # Progress bar
            # ----------------------------------

            progress = st.progress(0)

            # ----------------------------------
            # Status display
            # ----------------------------------

            status = st.empty()

            # ----------------------------------
            # Puzzle display
            # ----------------------------------

            board_display = st.empty()

            # ----------------------------------
            # Animate every solution step
            # ----------------------------------

            for step, (state, move) in enumerate(
                solution,
                start=1
            ):

                board_display.code(
                    f"""
{state[0]} | {state[1]} | {state[2]}
-----------
{state[3]} | {state[4]} | {state[5]}
-----------
{state[6]} | {state[7]} | {state[8]}
"""
                )

                status.write(
                    f"🤖 AI Move {step}: **{move}**"
                )

                progress.progress(
                    step / len(solution)
                )

                time.sleep(0.5)

            # ----------------------------------
            # Update final puzzle
            # ----------------------------------

            st.session_state.puzzle = list(GOAL)

            st.success(
                "🏆 AI successfully solved the puzzle!"
            )


# ==========================================
# GOAL STATE
# ==========================================

st.divider()

st.subheader("🎯 Goal State")

st.code(
    """
1 | 2 | 3
-----------
4 | 5 | 6
-----------
7 | 8 | 0
"""
)


# ==========================================
# RESET
# ==========================================

if st.button(
    "🔄 Reset Puzzle",
    use_container_width=True
):

    st.session_state.puzzle = [
        1, 2, 3,
        4, 0, 6,
        7, 5, 8
    ]

    st.rerun()