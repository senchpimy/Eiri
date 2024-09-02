
# Virtual Assistant with Python Command Execution: EIRI

This project is a virtual assistant capable of executing Python commands with enhanced functionality for handling feedback, context, and memory.

## Features

- **Function Feedback**: The assistant provides feedback on the execution of functions. If a function executes successfully, it confirms this. In case of an error, it reports the issue along with the result.
  
- **Contextual Function Evaluation**: Context from previous interactions is passed to the function evaluator to improve the accuracy and relevance of function executions.
  
- **Request Coherence Check**: The assistant evaluates whether the user’s request is coherent before attempting to execute a function.
  
- **Memory Management**: The assistant maintains a memory of the last 5-7 messages related to function executions, which helps in keeping track of the ongoing tasks and context.
  
- **Command Evaluation**: Improves the assistant's prompt and limits attempts to avoid unexpected outputs, like returning 'I' when a true/false decision is required. 

## Supported Models

- **Tested and Functional**:
  - phi3
  - llama3

- **Functional with Some Errors**:
  - **mistral**: Struggles with providing accurate arguments.
  - **wizardlm2**: Fails to evaluate if a function is needed.
  - **dolphin-mistral**: Occasionally fails to select the correct function.
  - **orca-mini**: Does not always evaluate when a function is needed.
