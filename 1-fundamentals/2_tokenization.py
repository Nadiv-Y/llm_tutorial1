from transformers import AutoTokenizer


tokenizer = AutoTokenizer.from_pretrained("gpt2")


text = "Hello, how are you?"

print("Text:", text)

token_ids = tokenizer.encode(text)
print("Token IDs:", token_ids) 


decoded_text = tokenizer.decode(token_ids)
print("Decoded Text:", decoded_text)


examples = ["antigravity", "unconstitutionally", "ingeniurious", "12345"]

for example in examples:
    token_ids = tokenizer.encode(example)
    print("Text:", example)
    print("Token IDs:", token_ids)
    print("Chunks:", tokenizer.convert_ids_to_tokens(token_ids))
    decoded_text = tokenizer.decode(token_ids)
    print("Decoded Text:", decoded_text)
    print()

