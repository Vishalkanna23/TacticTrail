
from app.ingestion.document_search import search_documents

QUESTIONS = [
    "What does NIST recommend for cybersecurity incident response?",
    "What should an incident response policy and plan include?",
    "How should organizations prepare for cybersecurity incidents?",
]


def calculate_hit_rate(question_hits: list[bool]) -> float:
    if not question_hits:
        return 0.0

    return sum(question_hits) / len(question_hits)


def main():
    question_hits = []

    for number, question in enumerate(QUESTIONS, start=1):
        print(f"\n{'=' * 60}")
        print(f"Question {number}: {question}")

        results = search_documents(question, top_k=3)

        found_relevant = False

        if not results:
            print("No chunks retrieved.")

        for rank, result in enumerate(results, start=1):
            print(f"\nRank: {rank}")
            print(f"Document: {result['document']}")
            print(f"Page: {result['page']}")
            print(f"Score: {result['similarity_score']:.4f}")
            print(f"Text:\n{result['text']}")

            while True:
                label = input(
                    "\nIs this chunk relevant? (y/n): "
                ).strip().lower()

                if label in ("y", "n"):
                    break

                print("Please enter y or n.")

            if label == "y":
                found_relevant = True

        question_hits.append(found_relevant)

    hit_rate = calculate_hit_rate(question_hits)

    print("\n===== Evaluation Results =====")
    print(f"Questions evaluated: {len(question_hits)}")
    print(f"Questions with hits: {sum(question_hits)}")
    print(f"Hit Rate@3: {hit_rate:.2%}")


if __name__ == "__main__":
    main()
