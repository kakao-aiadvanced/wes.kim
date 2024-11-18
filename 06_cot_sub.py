from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": dedent("""
                # Simple - 2
                Solve the following problem step-by-step: 123 - 58

                Step-by-step solution:
                1. First, 123 - 8 = 123 - 3 - 5.
                2. So, obviously, we get 120 - 5 = 115.
                3. 115 - 50 = 115 - 15 - 35.
                4. Thus, the answer equals 100 - 35.

                Answer:
            """),
        },
    ],
)

print(completion.choices[0].message)
