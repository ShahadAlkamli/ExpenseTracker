from django.test import TestCase
from django.urls import reverse
from .models import Transaction

class TransactionTestCase(TestCase):
    def setUp(self):
        self.transaction1 = Transaction.objects.create(text='Transaction 1', amount=100)
        self.transaction2 = Transaction.objects.create(text='Transaction 2', amount=-50)

    def test_transaction_creation(self):
        self.assertEqual(self.transaction1.text, 'Transaction 1')
        self.assertEqual(self.transaction1.amount, 100)
        self.assertEqual(self.transaction2.text, 'Transaction 2')
        self.assertEqual(self.transaction2.amount, -50)

    def test_transaction_list_view(self):
        response = self.client.get(reverse('transaction-list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transaction 1')
        self.assertContains(response, 'Transaction 2')

    def test_transaction_detail_view(self):
        response = self.client.get(reverse('transaction-detail', args=[self.transaction1.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Transaction 1')
        self.assertNotContains(response, 'Transaction 2')

    def test_add_transaction_view(self):
        data = {'text': 'New Transaction', 'amount': 75}
        response = self.client.post(reverse('transaction-list'), data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Transaction.objects.last().text, 'New Transaction')

    def test_delete_transaction_view(self):
        response = self.client.delete(reverse('transaction-detail', args=[self.transaction2.id]))
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Transaction.objects.filter(id=self.transaction2.id).exists())
