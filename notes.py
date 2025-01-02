# notes.py

from flask import abort, make_response
from config import db
from models import Note, NoteSchema, Person


def read_one(note_id):
    note = Note.query.get(note_id)

    print(note_id)
    print(note)
    note_schema = NoteSchema()


    if note is not None:
        result = note_schema.dump(note)
        print(result)

        return result
    else:
        abort(
            404, f"Note with ID {note_id} not found"
        )
# Update a note
def update(note_id, note):
    existing_note = Note.query.get(note_id)
    note_schema = NoteSchema()

    print(note)

    if existing_note:
        update_note = note_schema.load(note, session=db.session)  # Deserialize and load the new data
        existing_note.content = update_note.content  # Update the content
        db.session.merge(existing_note)  # Merge the updated object into the session
        db.session.commit()  # Commit the transaction
        return note_schema.dump(existing_note), 201  # Return the updated note
    else:
        abort(404, f"Note with ID {note_id} not found")

# Delete a note
def delete(note_id):
    existing_note = Note.query.get(note_id)

    if existing_note:
        db.session.delete(existing_note)  # Delete the note from the session
        db.session.commit()  # Commit the transaction
        return make_response(f"{note_id} successfully deleted", 204)  # Return a success message
    else:
        abort(404, f"Note with ID {note_id} not found")

# notes.py



def create(note):
    person_id = note.get("person_id")
    person = Person.query.get(person_id)
    note_schema = NoteSchema()


    if person:
        print(note)

        new_note = note_schema.load(note, session=db.session)
        print(new_note)
        person.notes.append(new_note)
        db.session.commit()
        return note_schema.dump(new_note), 201
    else:
        abort(404, f"Person not found for ID: {person_id}")
