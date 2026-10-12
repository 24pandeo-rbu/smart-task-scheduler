
# app.py
# Smart Task Scheduling and Resource Allocation System

import pandas as pd
import streamlit as st

from algorithms import (
    validate_tasks,
    priority_order,
    topological_sort,
    create_dependency_schedule,
    greedy_deadline_schedule,
    knapsack_allocation,
)

st.set_page_config(
    page_title="Smart Task Scheduler",
    page_icon="📅",
    layout="wide",
)

st.title("📅 Smart Task Scheduling & Resource Allocation")
st.write(
    "Explore priority queues, dependency graphs, greedy scheduling, "
    "and dynamic programming through an interactive task planner."
)

st.info(
    "This is a simulated scheduling tool. Deadline scheduling "
    "assumes independent, one-slot jobs; dependency scheduling "
    "uses task durations and prerequisites."
)

SAMPLE_TASKS = [
    {
        "id": "T1",
        "name": "Design database",
        "duration": 2,
        "deadline": 3,
        "priority": 5,
        "value": 80,
        "dependencies": [],
    },
    {
        "id": "T2",
        "name": "Build API",
        "duration": 3,
        "deadline": 7,
        "priority": 4,
        "value": 100,
        "dependencies": ["T1"],
    },
    {
        "id": "T3",
        "name": "Create interface",
        "duration": 2,
        "deadline": 6,
        "priority": 3,
        "value": 70,
        "dependencies": ["T1"],
    },
    {
        "id": "T4",
        "name": "Write documentation",
        "duration": 1,
        "deadline": 5,
        "priority": 2,
        "value": 40,
        "dependencies": [],
    },
    {
        "id": "T5",
        "name": "Run final tests",
        "duration": 2,
        "deadline": 10,
        "priority": 5,
        "value": 90,
        "dependencies": ["T2", "T3"],
    },
]

if "tasks" not in st.session_state:
    st.session_state.tasks = [dict(t) for t in SAMPLE_TASKS]


def reset_tasks():
    st.session_state.tasks = [dict(t) for t in SAMPLE_TASKS]


def parse_dependencies(text):
    return [
        item.strip()
        for item in text.split(",")
        if item.strip()
    ]


st.sidebar.header("Task Controls")

if st.sidebar.button("Restore sample tasks"):
    reset_tasks()

st.sidebar.caption(
    "You can edit task details in the table below. "
    "Use comma-separated task IDs for dependencies."
)

st.subheader("1. Task List")

st.caption(
    "Edit the table and click outside a cell to apply changes. "
    "Dependencies are task IDs, such as T1 or T2,T3."
)

table_rows = []

for task in st.session_state.tasks:
    table_rows.append({
        "ID": task["id"],
        "Task": task["name"],
        "Duration": task["duration"],
        "Deadline": task["deadline"],
        "Priority": task["priority"],
        "Value": task["value"],
        "Dependencies": ", ".join(task["dependencies"]),
    })

edited = st.data_editor(
    pd.DataFrame(table_rows),
    num_rows="dynamic",
    use_container_width=True,
    hide_index=True,
    key="task_editor",
    column_config={
        "ID": st.column_config.TextColumn(
            "ID", help="Unique ID, e.g. T6"
        ),
        "Task": st.column_config.TextColumn("Task name"),
        "Duration": st.column_config.NumberColumn(
            "Duration (time units)", min_value=1, step=1
        ),
        "Deadline": st.column_config.NumberColumn(
            "Deadline (time units)", min_value=1, step=1
        ),
        "Priority": st.column_config.NumberColumn(
            "Priority", min_value=1, step=1
        ),
        "Value": st.column_config.NumberColumn(
            "Value", min_value=0, step=10
        ),
        "Dependencies": st.column_config.TextColumn(
            "Dependencies", help="For example: T1,T2"
        ),
    },
)

if st.button("Apply task changes", type="primary"):
    try:
        tasks = []

        for row in edited.to_dict("records"):
            task_id = str(row["ID"]).strip()
            name = str(row["Task"]).strip()

            if not task_id or not name:
                raise ValueError("Task IDs and names cannot be empty.")

            for field in ["Duration", "Deadline", "Priority", "Value"]:
                number = float(row[field])

                if not number.is_integer():
                    raise ValueError(f"{field} must be a whole number.")

            tasks.append({
                "id": task_id,
                "name": name,
                "duration": int(row["Duration"]),
                "deadline": int(row["Deadline"]),
                "priority": int(row["Priority"]),
                "value": int(row["Value"]),
                "dependencies": parse_dependencies(
                    str(row["Dependencies"])
                ),
            })

        validate_tasks(tasks)
        topological_sort(tasks)

        st.session_state.tasks = tasks
        st.success("Task list updated successfully.")
        st.rerun()

    except (ValueError, TypeError, KeyError) as error:
        st.error(f"Could not apply changes: {error}")


tasks = st.session_state.tasks

try:
    validate_tasks(tasks)
    dependency_order = topological_sort(tasks)
    task_by_id = {task["id"]: task for task in tasks}

    st.subheader("2. Dependency-Aware Schedule")

    st.write(
        "Tasks are arranged so that prerequisites finish before "
        "dependent tasks begin. A late task is flagged if its "
        "calculated finish time exceeds its deadline."
    )

    schedule = create_dependency_schedule(tasks)

    if schedule:
        st.dataframe(
            pd.DataFrame(schedule),
            use_container_width=True,
            hide_index=True,
        )

        on_time = sum(
            item["Status"] == "On time" for item in schedule
        )
        late = len(schedule) - on_time

        c1, c2, c3 = st.columns(3)
        c1.metric("Total tasks", len(schedule))
        c2.metric("On time", on_time)
        c3.metric("Late", late)

    st.subheader("3. Priority Queue")

    order = priority_order(tasks)
    st.write(
        "Priority queue order (highest priority first, then "
        "earliest deadline). This is a ranking, not a schedule "
        "that automatically enforces dependencies."
    )
    st.write(" → ".join(order) if order else "No tasks")

    st.subheader("4. Greedy Deadline Scheduling")

    st.write(
        "For this experiment only, each task is treated as an "
        "independent job that occupies one time slot. The algorithm "
        "selects high-value jobs that fit before their deadlines."
    )

    one_slot_jobs = [
        task for task in tasks if task["duration"] == 1
    ]

    if one_slot_jobs:
        greedy_result = greedy_deadline_schedule(one_slot_jobs)

        if greedy_result:
            st.dataframe(
                pd.DataFrame(greedy_result),
                use_container_width=True,
                hide_index=True,
            )
            st.metric(
                "Total selected value",
                sum(item["Value"] for item in greedy_result),
            )
        else:
            st.write("No jobs could be scheduled.")
    else:
        st.warning(
            "There are no one-slot tasks. Edit a task's duration "
            "to 1 to try this algorithm."
        )

    st.subheader("5. Resource Allocation with Dynamic Programming")

    capacity = st.slider(
        "Available time budget (time units)",
        min_value=0,
        max_value=30,
        value=6,
    )

    allocation = knapsack_allocation(tasks, capacity)

    m1, m2, m3 = st.columns(3)
    m1.metric("Selected tasks", len(allocation["tasks"]))
    m2.metric("Total time used", allocation["total_duration"])
    m3.metric("Total value", allocation["total_value"])

    if allocation["tasks"]:
        st.dataframe(
            pd.DataFrame([
                {
                    "Task": task["name"],
                    "Duration": task["duration"],
                    "Value": task["value"],
                }
                for task in allocation["tasks"]
            ]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.write("No tasks selected for this budget.")

    st.caption(
        "Knapsack optimizes value under a time budget. It does "
        "not enforce deadlines or task dependencies; those are "
        "handled in the separate dependency-aware schedule."
    )

    st.subheader("6. Dependency Order")

    st.write(" → ".join(dependency_order) if dependency_order else "No tasks")

    st.subheader("7. Algorithm Complexity")

    st.table(pd.DataFrame([
        {
            "Algorithm": "Priority queue",
            "Purpose": "Rank tasks by priority",
            "Typical complexity": "O(n log n)",
        },
        {
            "Algorithm": "Topological sort",
            "Purpose": "Respect prerequisites",
            "Typical complexity": "O(V + E)",
        },
        {
            "Algorithm": "Greedy deadline scheduling",
            "Purpose": "Schedule unit-time jobs by value",
            "Typical complexity": "O(n log n + nD)",
        },
        {
            "Algorithm": "0/1 Knapsack DP",
            "Purpose": "Maximize value under a budget",
            "Typical complexity": "O(nC)",
        },
    ]))

    st.caption(
        "Here n is the number of tasks, V the number of graph "
        "vertices, E the number of dependency edges, D the maximum "
        "deadline, and C the integer resource capacity."
    )

except ValueError as error:
    st.error(f"Scheduling error: {error}")
    st.info(
        "Check that task IDs are unique, dependencies exist, "
        "and the dependency graph has no cycles."
    )

st.divider()
st.caption(
    "Smart Task Scheduling & Resource Allocation | "
    "Python • Heaps • Graphs • Greedy Algorithms • Dynamic Programming"
)
