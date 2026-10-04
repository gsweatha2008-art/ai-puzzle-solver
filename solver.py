import heapq


# ==========================================
# MANHATTAN DISTANCE
# ==========================================

def manhattan_distance(state, goal):

    distance = 0

    for index in range(9):

        value = state[index]

        # 0 represents the empty space
        if value == 0:
            continue

        current_row = index // 3
        current_col = index % 3

        goal_index = goal.index(value)

        goal_row = goal_index // 3
        goal_col = goal_index % 3

        distance += abs(current_row - goal_row)
        distance += abs(current_col - goal_col)

    return distance


# ==========================================
# GENERATE POSSIBLE MOVES
# ==========================================

def get_neighbors(state):

    neighbors = []

    # Find empty space
    zero_index = state.index(0)

    row = zero_index // 3
    col = zero_index % 3

    moves = {
        "Up": (-1, 0),
        "Down": (1, 0),
        "Left": (0, -1),
        "Right": (0, 1)
    }

    for move, (row_change, col_change) in moves.items():

        new_row = row + row_change
        new_col = col + col_change

        # Check valid position
        if 0 <= new_row < 3 and 0 <= new_col < 3:

            new_index = new_row * 3 + new_col

            new_state = list(state)

            # Swap empty space and tile
            new_state[zero_index], new_state[new_index] = (
                new_state[new_index],
                new_state[zero_index]
            )

            neighbors.append(
                (tuple(new_state), move)
            )

    return neighbors


# ==========================================
# A* SEARCH ALGORITHM
# ==========================================

def solve_puzzle(start, goal):

    priority_queue = []

    # g = cost from start
    g = 0

    # h = estimated cost to goal
    h = manhattan_distance(start, goal)

    # f = total cost
    f = g + h

    heapq.heappush(
        priority_queue,
        (f, g, start, [])
    )

    visited = set()

    while priority_queue:

        f, g, current, path = heapq.heappop(
            priority_queue
        )

        # Goal reached
        if current == goal:
            return path

        if current in visited:
            continue

        visited.add(current)

        # Generate next states
        for neighbor, move in get_neighbors(current):

            if neighbor not in visited:

                new_g = g + 1

                new_h = manhattan_distance(
                    neighbor,
                    goal
                )

                new_f = new_g + new_h

                new_path = path + [
                    (neighbor, move)
                ]

                heapq.heappush(
                    priority_queue,
                    (
                        new_f,
                        new_g,
                        neighbor,
                        new_path
                    )
                )

    return None