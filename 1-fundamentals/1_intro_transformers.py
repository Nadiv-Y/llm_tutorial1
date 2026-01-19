from transformers import pipeline

generator = pipeline(task="text-generation", model="gpt2")

prompt = "The future of artificial intelligence is "


response = generator(prompt, max_new_tokens=50, num_return_sequences=2, pad_token_id=generator.tokenizer.eos_token_id)
for i, r in enumerate(response, start=1):
    print(f"Response {i}: {r['generated_text']}")   