from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": dedent("""
                # Simple - 1
                Solve the following problem step-by-step: 23 + 47

                Step-by-step solution:
                1. 3 + 7 equals 10.
                2. Because it's greater than 9, the last digit is 10 (the result) - 10 = 0.
                3. The extra 1 gets added up with 2 and 4.
                4. Tenth digit is 7 = 2 + 4 + 1.

                Answer:
            """),
        },
    ],
)

print(completion.choices[0].message)
