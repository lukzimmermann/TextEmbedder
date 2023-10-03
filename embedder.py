from src import embeddingOpenAI
from src import pdfText
from src import fileHandler
from src import postgres

fileHandler = fileHandler.FileHandler()


for file in fileHandler.fileList:
    if file.isUpToDate is False:
        print("Actual File: " + file.name)
        pages = pdfText.getPages(file.fullpath)
        pageCounter = 0
        for page in pages:
            dataSet = embeddingOpenAI.createEmbedding(page)
            if dataSet is not None:
                if len(dataSet.vector) == 1536:
                    pg = postgres.PostgresDB()
                    pg.connect()
                    vector = dataSet.vector.tolist() 
                    data = (file.id, pageCounter, page, dataSet.tokens, vector)
                    pg.executeQuery(f"""INSERT INTO embedding
                                    (doc_id, doc_segment, doc_text, tokens, embedding_ada002)
                                    VALUES (%s, %s, %s, %s, %s::vector)""", data)
                    pg.disconnect()
                else:
                    print(f"ERROR: Vector length is NOT correct! Length: {len(dataSet.vector)}\tToken: {dataSet.tokens}")
                pageCounter += 1