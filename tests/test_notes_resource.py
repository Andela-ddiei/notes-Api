import json
import time

from base_test import BaseTest
from models import db, Note


class NoteResource(BaseTest):

    def test_get_notes(self):
        token = self.get_token(self.user.username, self.password)

        note1 = Note(title=self.fake.sentence(), content=self.fake.paragraph())
        note2 = Note(title=self.fake.sentence(), content=self.fake.paragraph())

        note1.user_id = self.user.id
        note2.user_id = self.user.id

        db.session.add(note1)
        db.session.add(note2)
        db.session.commit()

        response = self.client.get("/notes", headers={"Authorization": token})
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data.decode("ascii"))
        decoded_response = response.data.decode("ascii")
        self.assertEqual(len(response_data), 2)
        self.assertTrue(note1.title in decoded_response)
        self.assertTrue(note1.content in decoded_response)
        self.assertTrue(note2.title in decoded_response)
        self.assertTrue(note2.content in decoded_response)

    def test_no_created_notes(self):
        token = self.get_token(self.user.username, self.password)

        response = self.client.get("/notes", headers={"Authorization": token})
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data.decode("ascii"))
        self.assertTrue("No notes have been created" in response_data["message"])

    def test_create_notes(self):
        token = self.get_token(self.user.username, self.password)

        note = {
            "title": self.fake.sentence(),
            "content": self.fake.paragraph()
        }
        response = self.client.post("/notes", data=json.dumps(note), content_type="application/json", headers={"Authorization": token})
        self.assertEqual(201, response.status_code)
        user_id = Note.query.get(1).user_id
        response_data = json.loads(response.data.decode("ascii"))
        self.assertTrue("title" in response_data)
        self.assertTrue("user_id" in response_data)

    def test_update_notes(self):
        token = self.get_token(self.user.username, self.password)

        note = Note(title=self.fake.sentence(), content=self.fake.paragraph())
        note.user_id = self.user.id


        db.session.add(note)
        db.session.commit()

        old_note_title = Note.query.get(1).title

        update = {
            "title": self.fake.sentence()
        }
        response = self.client.put("/notes/1", data=json.dumps(update), content_type="application/json", headers={"Authorization": token})
        new_note_title = Note.query.get(1).title
        self.assertEqual(200, response.status_code)
        response_data = json.loads(response.data.decode("ascii"))
        self.assertNotEqual(old_note_title, new_note_title)

    def test_delete_notes(self):
        token = self.get_token(self.user.username, self.password)

        note = Note(title=self.fake.sentence(), content=self.fake.paragraph())

        note.user_id = self.user.id

        db.session.add(note)
        db.session.commit()

        response = self.client.delete("/notes/1", headers={"Authorization": token})
        self.assertEqual(204, response.status_code)
