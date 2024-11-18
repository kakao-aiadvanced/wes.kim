from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": dedent("""
                movie: 영화
                restaurant: 식당
                notebook: 공책
                electricity: 전기
                happy: 행복하다
            """),
        },
        {
            "role": "user",
            "content": "dog:"
        },
    ],
)

print(completion.choices[0].message)
