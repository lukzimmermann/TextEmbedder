import openai
from src import embeddingOpenAI
from src import postgres

userPrompt = "Welche Unendlichkeit sind abzählbar"

dataSet = embeddingOpenAI.createEmbedding(userPrompt)


class Document:
    def __init__(self):
        self.id = 0
        self.name = ''
        self.page = 0
        self.tags = []
        self.text = 0

def getTagsById(id):
    tags = []
    pg = postgres.PostgresDB()
    pg.connect()
    data = (id,)
    response = pg.selectQuery(f"""
                    SELECT tag
                    FROM tag
                    WHERE doc_id = %s""",
                    data)
    pg.disconnect()

    for item in response:
        tags.append(item[0])
    return tags

def getTextFromDataBase(vector):
    pg = postgres.PostgresDB()
    pg.connect()
    vector = dataSet.vector.tolist() 
    data = (vector,)

    response = pg.selectQuery(f"""
                    SELECT doc_id, filename, doc_segment, doc_text
                    FROM embedding
                    JOIN document ON id = doc_id
                    ORDER BY embedding_ada002 <-> %s::vector 
                    LIMIT 5;""",
                    data)
    pg.disconnect()

    documents = []

    for item in response:
        document = Document()
        document.id = item[0]
        document.name = item[1]
        document.page = item[2]
        document.text = item[3]
        document.tags = getTagsById(document.id)
        documents.append(document)
    
    return documents

documents = getTextFromDataBase(dataSet.vector)
context = ""

sourceCounter = 1
context += "Das sind verschiedene Quellen auf die dich referenzieren sollst. Falls du diese Quellen verwendest, gibt den Namen und die page an auf die du dich referenzierst\n\n"
for doc in documents:
    context += f"Quelle: {sourceCounter}\nDocument: {doc.name}\nPage: {doc.page+1}\nTags: {doc.tags}\nText: {doc.text}\n\n\n"
    sourceCounter += 1


prompt = f"""
{context}
UserPromt: {userPrompt}
"""

for doc in documents:
    print(f"Document: {doc.name}\nPage: {doc.page}\nTags: {doc.tags}\nText: {doc.text}\n\n")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]
)
print("Prompt: ", userPrompt)
print("")
print({response["choices"][0]["message"]["content"]})

