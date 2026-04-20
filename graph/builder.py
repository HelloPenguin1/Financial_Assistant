from langgraph.graph import StateGraph, START, END
from .state import GraphState
from nodes.query_decomposer import QueryDecomposer
from nodes.constructDB import Construct_DB
from nodes.orchestrator_worker import orchestrator, assign_workers, llm_call, synthesizer
from nodes.interpreter import retriever, llm_response
from nodes.route_decision import route_decision


# Initialize the graph
graph = StateGraph(GraphState)
construct_db = Construct_DB()

# Add nodes
graph.add_node("query_decomposer",QueryDecomposer)
graph.add_node("constructdb", construct_db.build_vectordb)
graph.add_node("orchestrator", orchestrator)
graph.add_node("retriever", retriever)  #To be fixed to corret name
graph.add_node("llm_response", llm_response)
graph.add_node("llm_call", llm_call)
graph.add_node("synthesizer", synthesizer)

#Add edges
graph.add_edge(START, "query_decomposer")
graph.add_edge("query_decomposer", "constructdb")
graph.add_conditional_edges("constructdb", 
                            route_decision, 
                            {
                                'orchestrator':'orchestrator',
                                'retriever':'retriever'
                            })

graph.add_conditional_edges(
    "orchestrator",
    assign_workers,  #possibly optimize
    ["llm_call"]
)

graph.add_edge("retriever", "llm_response")
graph.add_edge("llm_response", END)

#temp

graph.add_edge("llm_call", "synthesizer")
graph.add_edge("synthesizer", END)



# Compile
workflow = graph.compile()



if __name__ == "__main__":
    try:
        while True:
            question = input("Question: ")

            result = workflow.invoke({"query": question})
            print(result[:2000])
            
            
    except KeyboardInterrupt:
        print("\nExiting...")
