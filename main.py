import embeddingOpenAI
import pdfText
import fileHandler
import postgres

fileHandler = fileHandler.FileHandler()

if True:
    for file in fileHandler.fileList:
        print("Actual File: " + file.name)
        pages = pdfText.getPages(file.fullpath)
        counter = 0
        for page in pages:
            dataSet = embeddingOpenAI.createEmbedding(page)
            if dataSet is not None:
                if len(dataSet.vector) == 1536:
                    pg = postgres.PostgresDB()
                    pg.connect()
                    vectorAsString = dataSet.vector.tolist() 
                    data = (file.id, counter, page, dataSet.tokens, vectorAsString)
                    pg.executeQuery(f"""INSERT INTO embedding
                                    (doc_id, doc_segment, doc_text, tokens, embedding_ada002)
                                    VALUES (%s, %s, %s, %s, %s::vector)""", data)
                    pg.disconnect()
                else:
                    print(f"ERROR: Vector length is NOT correct! Length: {len(dataSet.vector)}\tToken: {dataSet.tokens}")
                counter += 1