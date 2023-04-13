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

        conversation = f"User: {prompt}\nAI: {response}"

        openai_result = openai.Completion.create(
            engine=OPENAI_SUMMARIZATION_MODEL,
            prompt=f"Summarize the following conversation into a list of semicolon separated key facts:\n{conversation}\n\nKey Facts (e.g FACT A KEY: FACT A VALUE; etc):",
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