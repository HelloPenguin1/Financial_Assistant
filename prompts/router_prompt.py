from langchain_core.prompts import ChatPromptTemplate, PromptTemplate


router_prompt = ChatPromptTemplate.from_template(
    """
   
    
    User Question : {question}
    
    """
    
)
