from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": dedent("""
                # Intermediate - 1
                Solve the following logic puzzle step-by-step:
                Three friends, Alice, Bob, and Carol, have different favorite colors: red, blue, and green. We know that:
                1. Alice does not like red.
                2. Bob does not like blue.
                3. Carol likes green.

                Determine the favorite color of each friend.

                Step-by-step solution:
                1. Carol likes green. This eliminates green as the candidate for other friends.
                2. Since Bob does not like blue, and green is taken by Carol, the only available color is red for Bob.
                3. As the only remaining color is blue, either for Alice or in the list, Alice likes blue.
            """),
        },
        {
            "role": "user",
            "content": "Answer:"
        },
    ],
)

print(completion.choices[0].message)
