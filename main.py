import embeddingOpenAI
import pdfText
import fileHandler
import postgres

fileHandler = fileHandler.FileHandler()

if True:
    for file in fileHandler.fileList:
        pages = pdfText.getPages(file.fullpath)
        counter = 0
        for page in pages:
            dataSet = embeddingOpenAI.createEmbedding(page)
            if dataSet is not None:
                pg = postgres.PostgresDB()
                pg.connect()
                vectorAsString = dataSet.vector.tolist() 
                data = (file.id, counter, page, dataSet.tokens, vectorAsString)
                print(vectorAsString)
                pg.executeQuery(f"""INSERT INTO embedding
                                (doc_id, doc_segment, doc_text, tokens, embedding_ada002)
                                VALUES (%s, %s, %s, %s, %s::vector)""", data)
                pg.disconnect()
                print(file.name)
                counter += 1