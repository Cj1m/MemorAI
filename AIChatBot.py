import openai
from Fact import Fact
from Config import DEBUG_MODE, OPENAI_MODEL, OPENAI_SYSTEM_PROMPT, OPENAI_SUMMARIZATION_MODEL

class AIChatBot:
    def __init__(self, database):
        self.database = database
        self.short_term_memory = []
        self.short_term_memory_limit = 10

    def interact(self, prompt):
        stored_data = self.database.fetch_related_data(prompt)
        context = self._build_context(stored_data)
        
        response = self._get_response_from_openai(context, prompt)
        self._update_short_term_memory("user", prompt)
        self._update_short_term_memory("assistant", response)

        facts = self._extract_facts_with_openai(prompt)
        for fact in facts:
            self.database.store_fact(fact)

        return response

    def _build_context(self, stored_data):
        context = [{"role": "system", "content": OPENAI_SYSTEM_PROMPT}] + stored_data + self.short_term_memory
        return context

    def _get_response_from_openai(self, context, prompt):
        openai_result = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            messages=context + [{"role": "user", "content": prompt}]
        )
        return openai_result.choices[0].message.content.strip()

    def _update_short_term_memory(self, speaker, message):
        message = {"role": speaker, "content": message}
        self.short_term_memory.append(message)

        if len(self.short_term_memory) > self.short_term_memory_limit:
            self.short_term_memory.pop(1)

    def _extract_facts_with_openai(self, prompt):
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
