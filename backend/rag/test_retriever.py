from retriever import retrieve_financial_context


question = input(
    "Enter a financial question: "
)


try:

    context = retrieve_financial_context(
        question
    )

    print("\n========== RAG CONTEXT ==========\n")

    print(context)

    print("\n=================================\n")


except Exception as e:

    print("\n❌ RAG ERROR")
    print(type(e).__name__)
    print(e)