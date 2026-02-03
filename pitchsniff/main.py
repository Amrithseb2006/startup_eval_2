from dotenv import load_dotenv
load_dotenv()

from graph.graph_builder import app
from utils.pretty_print import pretty_print_swot


def main():
    idea = input("Enter your startup idea:\n> ")

    final_state = app.invoke({
        "raw_idea": idea
    })

    print("\n==============================")
    print("     STARTUP EVALUATION")
    print("==============================")

    print(f"\nFinal Score: {final_state['final_score']}/100")

    print("\nMetric Scores:")
    for metric, score in final_state["metric_scores"].items():
        print(f"  {metric}: {score}/10")

    pretty_print_swot(final_state["swot_analysis"])


if __name__ == "__main__":
    main()
