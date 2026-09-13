"""
main.py

Entry point of the Health Assistant.
"""


from assistant import HealthAssistant
from config import OLLAMA_BASE_URL, API_KEY



def main():

    assistant = HealthAssistant(
        base_url=OLLAMA_BASE_URL,
        api_key=API_KEY
    )

    print("=" * 60)
    print("Health Assistant")
    print("Type 'quit' to exit.")
    print("=" * 60)

    while True:

        question = input("\nYou: ")

        if question.lower() in ["quit", "exit"]:
            break

        try:

            answer = assistant.ask(question)

            print("\nAssistant:")
            print(answer)

        except Exception as e:

            print("\nError:")
            print(e)


if __name__ == "__main__":
    main()
