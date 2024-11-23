from openai import OpenAI
import pandas as pd

client = OpenAI()

df = pd.read_csv("juice-shop_vulnerabilities_2024-11-14T1526.csv")


for _, row in df.iterrows():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You're a pentest generator"},
            {
                "role": "user",
                "content": f"Write a pentest using the python playwright package for the following vulnerability:\nVulnerability: {row['Vulnerability']}\nDetails: {row['Details']}\nWrite ONLY the working script.\n",
            },
        ],
    )

    print(completion.choices[0].message)
