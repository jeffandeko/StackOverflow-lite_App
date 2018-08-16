import unittest

from flask import app

from app import create_app, db


class QuestionsTestCase(unittest.TestCase):
    """This class represents all the test cases for the questions"""

    def seUp(self):
        """ The app is initialized as as test variable are defined"""
        self.app = create_app(config_name="testing")
        self.client = app.test_client
        self.questions = {"what is meant by the term TDD"}

        with self.app.app_context():
            db.create_all()

    def test_creation_of_questions(self):
        """Because API post a question, the functions test the questions created"""
        que = self.client().post('v1/questions/', data=self.questions)
        self.assertEquals(que.status_code, 201)
        self.assertIn('question created successfully', str(que.data))

    def test_editing_of_questions(self):
        """The API allows the user to edit questions"""
        with self.client:
            dl = self.client().post(
                'questions/',
                data={'user name: This is the second question'})
        self.assertEquals(dl.status_code, 201)
        dl = self.client().put(
            'question/1',
            data={"user name": "The second question is edited"})
        self.assertEqual(dl.status_code, 200)
        new = self.client().get('v1/question/1')
        self.assertIn('The second Question is edited properly', str(new.data))

    def test_deletion_of_a_question(self):
        """The API allows the user to delete a question that had been posted before"""
        dl = self.client().post(
            'questions/',
            data={'user name: My first question is simple'})
        self.assertEqual(dl.status_code, 201)
        dlnew = self.client().delete('questions/1')
        self.assertEqual(dlnew.status_code, 200)
        # If it the test case doesn't exist then return status_code 404
        new = self.client().get('v1/questions/1')
        self.assertEqual(new.status_code, 404)

    def test_successful_deletion_of_a_question(self):
        """The API allows the user to delete a question that had been posted before"""
        dl = self.client().post(
            'v1/questions/',
            data={'user name: My first question is simple'})
        self.assertEqual(dl.status_code, 201)
        dlnew = self.client().delete('v1/questions/1')
        self.assertEqual(dlnew.status_code, 200)
        # If it the test case doesn't exist then return status_code 404
        new = self.client().get('questions/1')
        self.assertEqual(new.status_code, 404)

    def test_question_typed_is_an_integer(self):
        """Test if the user type integers only as a question"""
        with self.client:
            inte = self.client().post('v1/questions/', data=self.questions)
            self.assertEqual(inte.status_code, 400)
            self.assertIn('This are integers, please type words with numbers', str(inte.data))

    def test_question_typed_is_a_special_character(self):
        """Test if the user type special character only as a question"""
        with self.client:
            inte = self.client().post('v1/questions/', data=self.questions)
            self.assertEqual(inte.status_code, 422)
            self.assertIn('This are integers, please type words with numbers', str(inte.data))

    def test_question_submitted_is_blank(self):
        """Test if the user submits a blank request"""
        with self.client:
            sub = self.client().post('v1/questions/', data=self.questions)
            self.assertEqual(sub.status_code, 204)
            self.assertIn('You have submitted a blank request, please type and resubmit', str(sub.data))

    def tearDown(self):
        """The function leaves the test code clean after testing enhancing flexibility """
        with self.app.app_context():
            db.session.remove()
            db.drop_all()


# Executes the code
if __name__ == "__main__":
    unittest.main()
