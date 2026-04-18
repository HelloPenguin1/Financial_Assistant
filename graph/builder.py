from langgraph.graph import StateGraph, START, END
from .state import GraphState
from nodes.query_decomposer import QueryDecomposer, route_decision
from nodes.constructDB import Construct_DB
from nodes.orchestrator_worker import orchestrator, assign_workers, llm_call, synthesizer

# Initialize the graph
graph = StateGraph(GraphState)
construct_db = Construct_DB()

# Add nodes
graph.add_node("query_decomposer",QueryDecomposer)
graph.add_node("constructdb", construct_db.build_vectordb)
graph.add_node("orchestrator", orchestrator)
graph.add_node("llm_call", llm_call)
graph.add_node("synthesizer", synthesizer)

#Add edges
graph.add_edge(START, "query_decomposer")
graph.add_conditional_edges("query_decomposer", route_decision)



# Compile
workflow = graph.compile()



if __name__ == "__main__":
    try:
        while True:
            question = input("Question: ")

            result = workflow.invoke({"query": question})
            
            
            
            
            
            print(result["company"])
            print(result["filing_to_fetch"])
            print(result["rationale"])
            print(result["start_date"])
            print(result["end_date"])
            
    except KeyboardInterrupt:
        print("\nExiting...")
