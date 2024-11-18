from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": dedent("""
                This is an absolute masterpiece -> POS
                meh -> NEG
                another example of film industry's enshittification -> NEG
                YOU MUST WATCH THIS RIGHT NOW. -> POS
                I'm not sure if I like this, but the overall aesthetic was so unique and charming. -> POS
            """),
        },
        {
            "role": "user",
            "content": "The storyline was dull and uninspiring. ->"
        },
    ],
)

print(completion.choices[0].message)
