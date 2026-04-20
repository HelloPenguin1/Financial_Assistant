from langgraph.graph import StateGraph, START, END
from .state import GraphState
from nodes.query_decomposer import QueryDecomposer
from nodes.constructDB import Construct_DB
from nodes.orchestrator_worker import orchestrator, assign_workers, llm_call, synthesizer
from nodes.interpreter import retriever
from nodes.route_decision import route_decision


# #When intent == full_report:

# fetch filings
# build vectorstore
# generate 3 structured sections
# spawn 3 workers
# each:
# filtered retrieval (10-K / 10-Q / 8-K)
# LLM analysis
# aggregate

# Initialize the graph
graph = StateGraph(GraphState)
construct_db = Construct_DB()

# Add nodes
graph.add_node("query_decomposer",QueryDecomposer)
graph.add_node("constructdb", construct_db.build_vectordb)
graph.add_node("orchestrator", orchestrator)
graph.add_node("retriever", retriever)  #To be fixed to corret name
graph.add_node("llm_call", llm_call)
graph.add_node("synthesizer", synthesizer)

#Add edges
graph.add_edge(START, "query_decomposer")
graph.add_edge("query_decomposer", "constructdb")
graph.add_edge("constructdb", "router")
graph.add_conditional_edges("router", 
                            route_decision, 
                            {
                                'full_report':'orchestrator',
                                'specific':'retriever'
                            }
)

graph.add_conditional_edges(
    "orchestrator",
    assign_workers,  #possibly optimize
    ["llm_call"]
)

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
