
# tests.py
# Run using: python -m unittest tests.py

import unittest

from algorithms import (
    validate_tasks,
    priority_order,
    topological_sort,
    create_dependency_schedule,
    greedy_deadline_schedule,
    knapsack_allocation,
)


def sample_tasks():
    return [
        {
            "id": "A", "name": "Design", "duration": 2,
            "deadline": 3, "priority": 5, "value": 40,
            "dependencies": [],
        },
        {
            "id": "B", "name": "Build", "duration": 3,
            "deadline": 8, "priority": 3, "value": 60,
            "dependencies": ["A"],
        },
        {
            "id": "C", "name": "Document", "duration": 1,
            "deadline": 5, "priority": 4, "value": 20,
            "dependencies": [],
        },
    ]


class TestSchedulingAlgorithms(unittest.TestCase):

    def test_priority_queue(self):
        order = priority_order(sample_tasks())
        self.assertEqual(order[0], "A")

    def test_topological_order_respects_dependency(self):
        order = topological_sort(sample_tasks())
        self.assertLess(order.index("A"), order.index("B"))

    def test_dependency_schedule(self):
        schedule = create_dependency_schedule(sample_tasks())
        by_id = {row["Task ID"]: row for row in schedule}

        self.assertLessEqual(
            by_id["A"]["Finish"],
            by_id["B"]["Start"]
        )

    def test_cycle_is_rejected(self):
        tasks = sample_tasks()
        tasks[0]["dependencies"] = ["B"]

        with self.assertRaises(ValueError):
            topological_sort(tasks)

    def test_unknown_dependency_is_rejected(self):
        tasks = sample_tasks()
        tasks[0]["dependencies"] = ["UNKNOWN"]

        with self.assertRaises(ValueError):
            validate_tasks(tasks)

    def test_greedy_deadline_schedule(self):
        jobs = [
            {
                "id": "A", "name": "A", "duration": 1,
                "deadline": 1, "value": 50,
            },
            {
                "id": "B", "name": "B", "duration": 1,
                "deadline": 2, "value": 30,
            },
            {
                "id": "C", "name": "C", "duration": 1,
                "deadline": 1, "value": 20,
            },
        ]

        result = greedy_deadline_schedule(jobs)
        self.assertEqual(
            sum(item["Value"] for item in result), 80
        )

    def test_knapsack_budget(self):
        result = knapsack_allocation(sample_tasks(), 3)

        self.assertLessEqual(result["total_duration"], 3)
        self.assertEqual(result["total_value"], 60)

    def test_empty_knapsack(self):
        result = knapsack_allocation([], 5)
        self.assertEqual(result["total_value"], 0)
        self.assertEqual(result["tasks"], [])


if __name__ == "__main__":
    unittest.main()
