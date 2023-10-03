import os
import postgres

class File:
    def __init__(self, name, path, lastModified):
        self.id = -1
        self.name = name
        self.path = path
        self.fullpath = path + "/" + name
        self.lastModified = lastModified
        self.isUpToDate = False

class FileHandler:
    MAX_TIMESTAMP = 2147483646

    def __init__(self):
        self.directoryList = self.readDirectoryList()
        self.fileList = self.getFilelist()
        self.writeNewFilesToDatabase()

    def readDirectoryList(self):
        directoryList = []
        with open('filelist.txt', 'r') as file:
            for line in file:
                directoryList.append(line.strip())  # Remove leading/trailing whitespace and print the line
        return directoryList

    def getFilelist(self):
        files = []
        for directory in self.directoryList:
            for root, dirs, files_in_dir in os.walk(directory):
                for filename in files_in_dir:
                    file_path = os.path.join(root, filename)
                    timestamp = os.path.getmtime(file_path)
                    parts = filename.split(".")
                    file_extension = parts[-1]
                    if file_extension == "pdf":
                        files.append(File(filename,root, timestamp))

        return files

    def getIdOfDocument(self, filename):
        pg = postgres.PostgresDB()
        pg.connect()
        response = pg.selectQuery(f'SELECT id FROM document WHERE filename = \'{filename}\'')
        pg.disconnect()
        if len(response) > 0:
            return response[0][0]
        else:
            return -1
    
    def getLastModifiedDate(self, filename):
        pg = postgres.PostgresDB()
        pg.connect()
        response = pg.selectQuery(f"""SELECT last_modified_date
                        FROM document
                        WHERE filename = \'{filename}\'""")
        pg.disconnect()
        if len(response) > 0:
            return response[0][0]
        else:
            return self.MAX_TIMESTAMP

    def writeNewFilesToDatabase(self):
        for file in self.fileList:
            index = self.getIdOfDocument(file.name)
            lastModifiedInDataBase = self.getLastModifiedDate(file.name)
            if index == -1 or lastModifiedInDataBase < file.lastModified:
                pg = postgres.PostgresDB()
                pg.connect()
                pg.executeQuery(f"""INSERT INTO document
                                (filename, path, last_modified_date)
                                VALUES (\'{file.name}\',\'{file.path}\', {file.lastModified})
                                RETURNING id""")
                pg.disconnect()

                index = self.getIdOfDocument(file.name)
                print(index)
            else:
                file.isUpToDate = True
            
            file.id = index