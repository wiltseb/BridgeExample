from NoteStorage import ConsoleWriter, CsvStorage, FileFolderStorage
from NoteInput import ConsoleInput, EditorInput
    

def main():
    console_input = EditorInput()
    storage = ConsoleWriter(console_input)
    storage.write_note()

if __name__=="__main__":
    main()