from backend.ai.financial_advisor import (
    get_financial_advice
)


def main():

    USER_ID = 1

    print("\n================================")
    print("          FINSIGHT AI")
    print("================================")
    print("Ask your financial question.")
    print("Type 'exit' to stop.\n")


    while True:

        question = input(
            "You: "
        ).strip()


        if question.lower() == "exit":

            print("\nGoodbye!")

            break


        if not question:

            print(
                "Please enter a question.\n"
            )

            continue


        try:

            print("\nThinking...\n")


            answer = get_financial_advice(
                user_id=USER_ID,
                question=question
            )


            print("FinSight AI:")
            print(answer)

            print()


        except Exception as e:

            print("\n❌ ERROR")

            print(
                f"{type(e).__name__}: {e}"
            )

            print()


if __name__ == "__main__":
    main()