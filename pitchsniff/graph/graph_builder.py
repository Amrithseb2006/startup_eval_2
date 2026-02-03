from langgraph.graph import StateGraph, START, END
from  nodes.idea_parser import idea_parser_node
from  nodes.aggregator import final_score_aggregation
from  nodes.swot_agent import swot_analysis_agent
from  agents.product_agent import product_originality_agent
from  agents.market_agent import market_demand_agent
from  agents.defensibility_agent import defense_moat_agent
from  agents.execution_agent import execution_feasibility_agent
from  state.startup_state import startup_evaluator_state

def build_graph():
    graph = StateGraph(startup_evaluator_state)

    graph.add_node("idea_parser", idea_parser_node)

    graph.add_node("product_agent", product_originality_agent)
    graph.add_node("market_agent", market_demand_agent)
    graph.add_node("moat_agent", defense_moat_agent)
    graph.add_node("execution_agent", execution_feasibility_agent)

    graph.add_node("aggregator", final_score_aggregation)
    graph.add_node("swot_agent", swot_analysis_agent)

    graph.add_edge(START,"idea_parser")
    graph.add_edge("idea_parser", "product_agent")
    graph.add_edge("idea_parser", "market_agent")
    graph.add_edge("idea_parser", "moat_agent")
    graph.add_edge("idea_parser", "execution_agent")
    graph.add_edge("product_agent", "aggregator")
    graph.add_edge("market_agent", "aggregator")
    graph.add_edge("moat_agent", "aggregator")
    graph.add_edge("execution_agent", "aggregator")
    graph.add_edge("aggregator", "swot_agent")
    graph.add_edge("swot_agent", END)

    return graph.compile()

app = build_graph()