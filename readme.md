A simple example of the Bridge design pattern.

NoteWriter is the "abstraction." It takes a NoteInput (the "implementation"), which provides a get_note() method
for getting the note to write.