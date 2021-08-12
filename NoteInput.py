import sys, tempfile, os
from subprocess import call
from abc import ABC, abstractmethod

class NoteInput(ABC):
    """
    The 'implementation' for the Bridge pattern.
    """
    @abstractmethod
    def get_note() -> str:
        pass

class ConsoleInput(NoteInput):
    """
    Obtains note input from the console
    """
    def get_note(self) -> str:
        return input("Enter note: ")

class EditorInput(NoteInput):
    """
    Obtains note input from the default editor (given by the EDITOR environment variable). Defaults to Vim.
    """

    EDITOR = os.environ.get('EDITOR','vim')

    def get_note(self) -> str:
        # Stolen from https://stackoverflow.com/questions/6309587/how-to-launch-an-editor-e-g-vim-from-a-python-script
        
        initial_message = "Enter note..."
        with tempfile.NamedTemporaryFile(suffix=".tmp", mode='r+') as tf:
            tf.write(initial_message)
            tf.flush()
            call([EditorInput.EDITOR, tf.name])

            tf.seek(0)
            return tf.read()
