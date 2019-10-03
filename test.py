from unittest import TestCase, main as unittest_main, mock
from app import app
from bson.objectid import ObjectId

sample_sneaker_id = ObjectId('666f6f2d6261722d71757578')
sample_sneaker = {
    'name': 'Bred 4',
    'brand': 'Jordan'
}

sample_form_data = {
    'name': sample_sneaker['name'],
    'brand': sample_sneaker['brand']
}

class SneakerCentralTests(TestCase):

    def setUp(self):

        self.client = app.test_client()

        app.config['TESTING'] = True

    def test_index(self):
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Sneaker', result.data)

    def test_new(self):
        result = self.client.get('/sneakers/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Save Sneaker', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_sneaker(self, mock_find):
        mock_find.return_value = sample_sneaker

        result = self.client.get(f'/sneakers/{sample_sneaker_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Bred 4', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_sneaker(self, mock_find):
        mock_find.return_value = sample_sneaker

        result = self.client.get(f'sneakers/{sample_sneaker_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Bred 4', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_create_sneaker(self, mock_insert):
        result = self.client.post('/sneakers', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_sneaker)

    # @mock.patch('pymongo.collection.Collection.update_one')
    # def test_update_sneaker(self, mock_update):
    #     result = self.client.post('/sneakers/{sample_sneaker_id}', data=sample_form_data)
    #
    #     self.assertEqual(result.status, '302 FOUND')
    #     mock_update.assert_called_with({'_id': sample_sneaker_id}, {'$set': sample_sneaker})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_sneaker(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/sneakers/{sample_sneaker_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'._id': sample_sneaker_id})


if __name__ == '__main__':
    unittest_main()
