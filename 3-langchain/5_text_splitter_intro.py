from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter


text = """FIRST word2 word3word4 78895
Word5 word6 word7 word8.

SECOND word10 word11 word12 word13 word14 word15 word16 ifg uerfyheui qweuiorqo qeyrh.


THIRD This is the first sentence of the paragraph. This is the second sentence which is a bit longer. This is the third sentence to reach thirty two words exactly right now, yes."""

char_splitter = CharacterTextSplitter(
    chunk_size=20,
    chunk_overlap=10,
    separator=" "
)

char_chunks = char_splitter.split_text(text) 

# print(f"Total chunks: {len(char_chunks)}")
# for i, chunk in enumerate(char_chunks, 1):
#     print(f"Chunk {i}: {len(chunk)} chars: {chunk}")


recursive_splitter = RecursiveCharacterTextSplitter(
    chunk_size=60,
    chunk_overlap=10,
    # separator=" "
)
#The default seperators \n\n \n " " ""

recursive_chunks = recursive_splitter.split_text(text)

print(f"Total chunks: {len(recursive_chunks)}")
for i, chunk in enumerate(recursive_chunks, 1):
    print(f"Chunk {i}: {len(chunk)} chars: {chunk}")