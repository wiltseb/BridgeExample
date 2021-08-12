from abc import abstractmethod, ABC
from NoteInput import NoteInput
from datetime import datetime

import os
import shutil


class NoteWriter(ABC):
    """
    The 'abstraction' for the Bridge pattern.
    """
    def __init__(self, note_input: NoteInput) -> None:
        self.note_input = note_input

    def write_note(self):
        note = self.note_input.get_note()
        date = datetime.now()
        self._write_note(note, date)
    
    @abstractmethod
    def _write_note(self, note: str, now: datetime):
        pass

class ConsoleWriter(NoteWriter):
    def _write_note(self, note: str, now: datetime):
        print(f'{now.strftime("%Y-%m-%d-%H:%M:%S")}: {note}')


class FileFolderStorage(NoteWriter):
    """
    Stores notes in individual files (named by an incrementing note id).
    Note files are stored in folders named with the day's date.
    """
    STORAGE_FOLDER: os.path = os.path.join(os.curdir, 'notes')
    NOTE_ID_FILE: os.path = os.path.join(STORAGE_FOLDER, 'current_note_id')
    NOTE_ID_TEMP_FILE: os.path = os.path.join(STORAGE_FOLDER, 'current_note_id.temp')

    def __init__(self, note_input: NoteInput) -> None:
        super().__init__(note_input)
        
    def _write_note(self, note: str, now: datetime):
        folder_path = self._get_current_folder(now)
        if not os.path.isdir(folder_path):
            os.makedirs(folder_path)

        note_id = self._get_and_update_note_id()
        note_path = os.path.join(self._get_current_folder(now), str(note_id))

        with open(note_path, 'w') as note_file:
            note_file.write(note)

        print(f'Wrote note with id {note_id}')

    def _get_current_folder(self, now: datetime):
        return os.path.join(FileFolderStorage.STORAGE_FOLDER, now.strftime('%Y-%m-%d'))

    def _get_and_update_note_id(self) -> os.path:
        if not os.path.exists(FileFolderStorage.NOTE_ID_FILE):
            current_id = 0
        else:
            with open(FileFolderStorage.NOTE_ID_FILE, 'r') as current_id_file:
                current_id = int(current_id_file.readline().strip())

        with open(FileFolderStorage.NOTE_ID_TEMP_FILE, 'w') as temp_file:
            temp_file.write(str(current_id + 1))
        
        shutil.move(FileFolderStorage.NOTE_ID_TEMP_FILE, FileFolderStorage.NOTE_ID_FILE)

        return current_id
        

class CsvStorage(NoteWriter):
    """
    Stores notes in a single csv file. Note entries have a 'date' and 'note' column.
    """
    STORAGE_FOLDER: os.path = os.path.join(os.curdir, 'csv_notes')
    NOTES_FILE: os.path = os.path.join(STORAGE_FOLDER, 'notes')

    def __init__(self, note_input: NoteInput) -> None:
        super().__init__(note_input)

    def _write_note(self, note: str, now: datetime) -> int:
        if not os.path.exists(CsvStorage.STORAGE_FOLDER):
            os.makedirs(CsvStorage.STORAGE_FOLDER)

        write_header = not os.path.exists(CsvStorage.NOTES_FILE)

        with open(CsvStorage.NOTES_FILE, 'a') as note_file:
            if write_header:
                note_file.write('date,note\n')

            # Must be able to store multi-line notes without screwing up the csv format
            escaped_note = note.replace('\n', '\\n')
            note_file.write(f'{now.strftime("%Y-%m-%d-%H:%M:%S")},{escaped_note}\n')

        print("Note written successfully!")
    
        



