
# algorithms.py
# Smart Task Scheduling and Resource Allocation System

import heapq
from collections import deque


def validate_tasks(tasks):
    """Check task IDs, durations, deadlines, and dependencies."""
    ids = [task["id"] for task in tasks]

    if len(ids) != len(set(ids)):
        raise ValueError("Task IDs must be unique.")

    known_ids = set(ids)

    for task in tasks:
        if task["duration"] < 1:
            raise ValueError("Task duration must be at least 1.")
        if task["deadline"] < 1:
            raise ValueError("Deadline must be at least 1.")
        if task["priority"] < 1:
            raise ValueError("Priority must be at least 1.")
        if task["value"] < 0:
            raise ValueError("Task value cannot be negative.")

        for dependency in task["dependencies"]:
            if dependency not in known_ids:
                raise ValueError(
                    f"Unknown dependency: {dependency}"
                )
            if dependency == task["id"]:
                raise ValueError("A task cannot depend on itself.")


def priority_order(tasks):
    """Use a heap to order ready tasks by priority."""
    heap = []

    for task in tasks:
        heapq.heappush(
            heap,
            (-task["priority"], task["deadline"], task["id"])
        )

    ordered = []

    while heap:
        _, _, task_id = heapq.heappop(heap)
        ordered.append(task_id)

    return ordered


def topological_sort(tasks):
    """Order tasks so that dependencies come first."""
    ids = [task["id"] for task in tasks]
    task_by_id = {task["id"]: task for task in tasks}

    indegree = {task_id: 0 for task_id in ids}
    dependents = {task_id: [] for task_id in ids}

    for task in tasks:
        for dependency in task["dependencies"]:
            if dependency not in indegree:
                raise ValueError(
                    f"Unknown dependency: {dependency}"
                )

            indegree[task["id"]] += 1
            dependents[dependency].append(task["id"])

    ready = deque(
        task_id for task_id in ids if indegree[task_id] == 0
    )
    result = []

    while ready:
        current = ready.popleft()
        result.append(current)

        for dependent in dependents[current]:
            indegree[dependent] -= 1

            if indegree[dependent] == 0:
                ready.append(dependent)

    if len(result) != len(ids):
        raise ValueError(
            "Dependency cycle detected. Check task dependencies."
        )

    return result


def create_dependency_schedule(tasks):
    """Create a dependency-respecting schedule in time units."""
    order = topological_sort(tasks)
    task_by_id = {task["id"]: task for task in tasks}
    finish_time = {}
    schedule = []

    for task_id in order:
        task = task_by_id[task_id]

        # A task can start only after all dependencies finish.
        start_time = max(
            (finish_time[dep] for dep in task["dependencies"]),
            default=0
        )

        finish = start_time + task["duration"]
        finish_time[task_id] = finish

        schedule.append({
            "Task": task["name"],
            "Task ID": task_id,
            "Start": start_time,
            "Finish": finish,
            "Deadline": task["deadline"],
            "Priority": task["priority"],
            "Status": (
                "On time" if finish <= task["deadline"]
                else "Late"
            ),
            "Dependencies": ", ".join(task["dependencies"]) or "None"
        })

    return schedule


def greedy_deadline_schedule(jobs):
    """
    Schedule independent, unit-duration jobs to maximize value.

    Each job must fit in one time slot and must be completed
    no later than its deadline. This function does not model
    multi-unit durations or task dependencies.
    """
    if any(job["duration"] != 1 for job in jobs):
        raise ValueError(
            "Greedy deadline scheduling requires duration = 1."
        )

    if any(job["deadline"] < 1 for job in jobs):
        raise ValueError("Deadlines must be at least 1.")

    ordered = sorted(
        jobs,
        key=lambda job: (-job["value"], job["id"])
    )

    if not ordered:
        return []

    max_deadline = min(
        max(job["deadline"] for job in ordered),
        len(ordered)
    )
    slots = [None] * (max_deadline + 1)

    for job in ordered:
        latest_slot = min(job["deadline"], max_deadline)

        for slot in range(latest_slot, 0, -1):
            if slots[slot] is None:
                slots[slot] = job
                break

    return [
        {
            "Slot": slot,
            "Task": slots[slot]["name"],
            "Value": slots[slot]["value"],
            "Deadline": slots[slot]["deadline"]
        }
        for slot in range(1, len(slots))
        if slots[slot] is not None
    ]


def knapsack_allocation(tasks, capacity):
    """
    0/1 knapsack: select tasks with maximum total value
    within a fixed integer capacity.

    Each task is either selected completely or not selected.
    """
    if capacity < 0:
        raise ValueError("Capacity cannot be negative.")

    if any(task["duration"] < 1 for task in tasks):
        raise ValueError("Durations must be positive.")

    if any(task["value"] < 0 for task in tasks):
        raise ValueError("Values cannot be negative.")

    if len(tasks) * (capacity + 1) > 2_000_000:
        raise ValueError(
            "Capacity is too large for this demo. "
            "Use a smaller capacity."
        )

    n = len(tasks)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i, task in enumerate(tasks, start=1):
        weight = task["duration"]
        value = task["value"]

        for cap in range(capacity + 1):
            dp[i][cap] = dp[i - 1][cap]

            if weight <= cap:
                dp[i][cap] = max(
                    dp[i][cap],
                    dp[i - 1][cap - weight] + value
                )

    chosen = []
    cap = capacity

    for i in range(n, 0, -1):
        if dp[i][cap] != dp[i - 1][cap]:
            task = tasks[i - 1]
            chosen.append(task)
            cap -= task["duration"]

    chosen.reverse()

    return {
        "tasks": chosen,
        "total_duration": sum(t["duration"] for t in chosen),
        "total_value": sum(t["value"] for t in chosen),
        "capacity": capacity
    }
