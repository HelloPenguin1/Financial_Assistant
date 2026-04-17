from langgraph.graph import StateGraph, START, END
from .state import GraphState
from nodes.query_decomposer import QueryDecomposer

# Initialize the graph
graph = StateGraph(GraphState)

# Add nodes
graph.add_node("query_decomposer",QueryDecomposer)

#Add edges
graph.add_edge(START, "query_decomposer")
graph.add_edge("query_decomposer", END)


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
