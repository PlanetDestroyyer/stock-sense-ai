from codes.main import agent_executor, process_agent_output

output = agent_executor.invoke({"input": "Tell me about Tesla stock performance"})
response = process_agent_output(output) 
print("################################################")
print(f"Processed response: {response}")