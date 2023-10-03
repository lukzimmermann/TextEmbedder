import os
import openai
import tiktoken
import numpy as np

class OpenAiDataSet:
    def __init__(self):
        self.tokens = 0
        self.vector = 0

MODEL = "text-embedding-ada-002"
MAX_TOKENS = 8192

def createEmbedding(text):
  openai.organization = os.getenv("OPENAI_ORGANISATION_ID")
  openai.api_key = os.getenv("OPENAI_API_KEY")

  dataSet = OpenAiDataSet()
  dataSet.tokens = getNumberOfTokens(text)

  if dataSet.tokens < MAX_TOKENS:
    response = openai.Embedding.create(
      model=MODEL,
      input=text
    )
    dataSet.vector = np.array(response['data'][0]['embedding'])
    dataSet.vector = np.array([3,4])

    return dataSet
  else:
     print("ERROR: Too many tokens!")
  
def getNumberOfTokens(string):
    encoding = tiktoken.encoding_for_model(MODEL)
    numbersOfToken = len(encoding.encode(string))
    return numbersOfToken