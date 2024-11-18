from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": dedent("""
                # Intermediate - 2
                Solve the following logic puzzle step-by-step:
                Four people (A, B, C, D) are sitting in a row. We know that:
                1. A is not next to B.
                2. B is next to C.
                3. C is not next to D.

                Determine the possible seating arrangements.

                Step-by-step solution:
                1. From the knowledge #2, we know that the result must include BC or CB as a subsequence.
                2. From the knowledge #1, subsequences of AB and BA are banned.
                3. From the knowledge #3, subsequences of CD and DC are banned.
                4. From the steps above, we could combine all the possible sequences.
            """),
        },
        {
            "role": "user",
            "content": "Possible arrangements:"
        },
    ],
)

print(completion.choices[0].message) # 특이사항: 말 드럽게 안 들어먹고 드럽게 못 맞춤 (문제 지문도 사실 틀려 있음)
