"""
(C) Copyright 2026 Boni Garcia (https://bonigarcia.github.io/)
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
 http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import os

from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, GEval
from deepeval.test_case import LLMTestCase, SingleTurnParams


def main():
    test_case = LLMTestCase(
        input="I was charged twice for order #12345. What should I do?",
        actual_output=(
            "Please contact billing so they can verify the duplicate charge before any refund is promised."
        ),
        expected_output=(
            "The reply should acknowledge the duplicate charge, route the case to billing, and avoid promising a refund."
        ),
        retrieval_context=[
            "Billing policy: duplicate charges must be verified by billing before a refund is promised.",
        ],
    )

    metrics = [
        AnswerRelevancyMetric(threshold=0.7),
        FaithfulnessMetric(threshold=0.7),
        GEval(
            name="Policy compliance",
            criteria=(
                "Determine whether the reply acknowledges the duplicate charge, routes the issue to billing, "
                "and avoids promising a refund before verification."
            ),
            evaluation_params=[
                SingleTurnParams.ACTUAL_OUTPUT,
                SingleTurnParams.EXPECTED_OUTPUT,
            ],
            threshold=0.7,
        ),
    ]

    print("--- DeepEval metrics ---")
    for metric in metrics:
        metric.measure(test_case)
        print(f"{metric.__class__.__name__}: score={metric.score:.2f}")
        print(f"Reason: {metric.reason}\n")


if __name__ == "__main__":
    main()
