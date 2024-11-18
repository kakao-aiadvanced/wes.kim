from openai import OpenAI
from textwrap import dedent

client = OpenAI()

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "user",
            "content": dedent("""
                Convert the following natural language requests into SQL queries:
                1. "List employees with salary greater than 50,000": SELECT * FROM employees WHERE salary > 50000;
                2. "All products with no stocks left?": SELECT * FROM products WHERE stock = 0;
                3. "Name of students with math score > 90": SELECT name FROM students WHERE math_score > 90;
                4. "List of orders that were placed within recent 30 days": SELECT * FROM orders WHERE order_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
                5. "All the cities and their customer counts from our customers list.": SELECT city, COUNT(*) FROM customers GROUP BY city;

                Request: "Find the average salary of employees in the marketing department."
                SQL Query:
            """),
        },
    ],
)

print(completion.choices[0].message)
