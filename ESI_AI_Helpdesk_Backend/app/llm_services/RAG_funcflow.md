## RAG Workflow

### Overview
The Retrieval-Augmented Generation (RAG) workflow is designed to enhance the chatbot's ability to provide accurate and contextually relevant responses by combining information retrieval with generative AI capabilities. The workflow integrates multiple components to retrieve relevant knowledge base (KB) documents and generate responses based on the retrieved information.

### Functional Flow
1. **User Input**:
   - The user submits a query via the `/chat` API endpoint.
   - The query is encapsulated in a `ChatRequest` object.

2. **Knowledge Base Retrieval**:
   - The `retrieve_kb` function in `retriever.py` is invoked.
   - This function performs a similarity search to find the most relevant documents from the knowledge base based on the user's query.

3. **Answer Generation**:
   - The `generate_answer` function in `llm.py` is called with the user's query and the retrieved documents.
   - This function uses a large language model (LLM) to generate a response by combining the query context with the retrieved knowledge.

4. **Prompt Engineering**:
   - The `prompts.py` module is used to structure the input for the LLM, ensuring that the query and retrieved documents are formatted effectively.

5. **Response Delivery**:
   - The generated response is returned to the API layer and sent back to the user.

### Component Interaction
```plaintext
main.py
  |
  V
api.py
  |
  V
retriever.py
  |
  V
llm.py
  |
  V
prompts.py
  |
  V
api.py
  |
  V
response
```

### Key Points
- **Retriever**: Ensures that the chatbot has access to the most relevant knowledge base documents.
- **LLM**: Generates human-like responses by leveraging the retrieved documents and user query.
- **Prompts**: Plays a critical role in guiding the LLM to produce accurate and context-aware answers.

### Benefits of RAG
- Combines the precision of information retrieval with the creativity of generative AI.
- Ensures responses are grounded in factual knowledge from the knowledge base.
- Enhances the chatbot's ability to handle complex queries effectively.



