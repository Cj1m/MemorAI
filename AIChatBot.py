import openai
from Fact import Fact
from Config import DEBUG_MODE, OPENAI_MODEL, OPENAI_SYSTEM_PROMPT, OPENAI_SUMMARIZATION_MODEL
PINECONE_INDEX_NAME= "memory"

class AIChatBot:
    def __init__(self, database):
        self.database = database

    def interact(self, prompt):
        stored_data = self.database.fetch_related_data(prompt)

        context = [{"role": "system", "content": OPENAI_SYSTEM_PROMPT}] + stored_data
        openai_result = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=context + [{"role": "user", "content": prompt}]
        )

        response = openai_result.choices[0].message.content.strip()

        facts = self.extract_facts_with_openai(prompt, response)
        for fact in facts:
            self.database.store_fact(fact)

        return response

    def extract_facts_with_openai(self, prompt, response):
        facts = []

        conversation = f"User: {prompt}"

        openai_result = openai.Completion.create(
            engine=OPENAI_SUMMARIZATION_MODEL,
            prompt=f"Please convert the following monolog into independent concept pairings, encapsulating the entire context in each pairing. The concept pairings will be stored among unrelated memories and must make sense on their own. If there is no useful information to convert, do not return anything: '{conversation}' Example: For input text: User: My name is Bob. I was born March 2nd 2023. I like Back to the future and my favourite food is Pizza The expected output is: User's name: Bob; User's favourite food: Pizza; User's likes movie: Back to the Future; User DOB: 2nd March 2023 For input text: User: Hi there The expected output is: N/A\n\nAnswer:",
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.5,
        )

        summary = openai_result.choices[0].text.strip()

        if DEBUG_MODE:
            print("\n")
            print(f"\t###Summary: {summary}")
            print("\n")

        fact_strings = summary.split(';')

        for fact_string in fact_strings:
            key_value = fact_string.split(':', 1)
            if len(key_value) == 2:
                key, value = key_value
                key, value = key.strip(), value.strip()

                facts.append(Fact(key, value))

        return facts