from unittest import TestCase, main as unittest_main
from app import app
from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

sample_streetwear_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_streetwear = {
    'brand': 'Gucci',
    'type': 'Shirt',
    'price': '$100.00',
    'type': 'Shirt',
    'size': 'large',
    'color': 'white',
}

sample_form_data = {
    'brand': sample_streetwear['brand'],
    'type': sample_streetwear['type'],
    'price': sample_streetwear['price'],
    'type': sample_streetwear['type'],
    'size': sample_streetwear['size'],
    'color': sample_streetwear['color']
}

class StreetwearsTests(TestCase):

    def setUp(self):
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_index(self):
        result = self.client.get('/sneakers/streetwears')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Streetwear', result.data)

    def test_new(self):
        result = self.client.get('/sneakers/streetwears/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Streetwear', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show(self, mock_find):
        mock_find.return_value = sample_streetwear

        result = self.client.get('/sneakers/streetwears/{sample_streetwear_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'$100.00', result.data)

    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit(self, mock_find):
        mock_find.return_value = sample_streetwear

        result = self.client.get(f'/sneakers/streetwears/{sample_streetwear_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'$100.00', result.data)

    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit(self, mock_insert):
        result = self.client.post('/sneakers/streetwears/submit', data=sample_form_data)

        # After submitting, should redirect to that playlist's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_streetwear)

    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update(self, mock_update):
        result = self.client.post(f'/sneakers/streetwears/{sample_streetwear_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_streetwear_id}, {'$set': sample_streetweart})

    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/sneakers/streetwears/{sample_streetwear_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_streetwear_id})


if __name__ == '__main__':
    unittest_main()
