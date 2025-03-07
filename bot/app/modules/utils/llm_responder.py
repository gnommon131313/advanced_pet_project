import os
from langgraph.graph import Graph
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama.llms import OllamaLLM


class LLMResponder:
    
    def query(self, knowledge_base: list, question: str) -> str:
        self._knowledge_base = knowledge_base
        self._question = question
        
        return self._create_workflow().invoke({})
    
    def _retrieve_relevant_documents(self, state_data) -> dict:
        # Любой способ получения релевантных данных на основе базы знаний 
        self._relevant_documents = self._knowledge_base
        
        return state_data
    
    def _generate_answer(self, state_data) -> dict:
        template = 'Question: {question}\n\nRelevant Documents:{relevant_documents}\n\nAnswer: "please answer only based on the data obtained from the documents."'
        prompt = ChatPromptTemplate.from_template(template)
        model = OllamaLLM(model=os.getenv("OllamaLLM"))
        chain = prompt | model
        state_data["full"] = chain.invoke({
            "question": self._question,
            "relevant_documents": self._relevant_documents,
        })
        state_data["exact"] = state_data["full"].split("</think>")[1]  # Без размышлений модели
        
        return state_data
    
    def _create_workflow(self):
        workflow = Graph()

        workflow.add_node("retrieve_relevant_documents", self._retrieve_relevant_documents)
        workflow.add_node("generate_answer", self._generate_answer)

        workflow.add_edge("retrieve_relevant_documents", "generate_answer")

        workflow.set_entry_point("retrieve_relevant_documents")
        workflow.set_finish_point("generate_answer")

        return workflow.compile()
    
    
llm_responder = LLMResponder()