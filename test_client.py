from client import call_llm

# simple fake chunk for testing
test_chunks = ["GDGC is a tech club at VIT Bhopal focused on developer technologies."]

response = call_llm(test_chunks, "What is GDGC?")

print("MODEL RESPONSE:\n", response)
