from django.test import TestCase
from django.core.cache import cache
from .models import MyModel, RelatedModel
from .managers import generate_cache_key
import logging

logger = logging.getLogger(__name__)

class CachingTestCase(TestCase):
    def setUp(self):
        # Clear the cache before each test
        cache.clear()

    def test_create_and_cache_model(self):
        # Create an instance of MyModel
        my_model = MyModel.objects.create(name="Test", description="This is a test.")

        # Retrieve the instance to ensure it's cached
        retrieved_instance = MyModel.objects.get(name="Test")
        self.assertEqual(retrieved_instance.description, "This is a test.")

        # Check the cache directly
        cache_key = generate_cache_key(MyModel, name="Test")
        cached_instance = cache.get(cache_key)
        logger.debug(f"Cache Key: {cache_key}, Cached Instance: {cached_instance}")
        self.assertIsNotNone(cached_instance)
        self.assertEqual(cached_instance.description, "This is a test.")

    def test_cache_invalidation_on_update(self):
        # Create an instance of MyModel
        my_model = MyModel.objects.create(name="Test", description="This is a test.")

        # Update the instance
        my_model.description = "This is an updated test."
        my_model.save()

        # Retrieve the updated instance to ensure cache invalidation
        updated_instance = MyModel.objects.get(name="Test")
        self.assertEqual(updated_instance.description, "This is an updated test.")

        # Check the cache directly
        cache_key = generate_cache_key(MyModel, name="Test")
        cached_instance = cache.get(cache_key)
        logger.debug(f"Cache Key: {cache_key}, Cached Instance: {cached_instance}")
        self.assertIsNotNone(cached_instance)
        self.assertEqual(cached_instance.description, "This is an updated test.")

    def test_cache_invalidation_on_delete(self):
        # Create an instance of MyModel
        my_model = MyModel.objects.create(name="Test", description="This is a test.")

        # Delete the instance
        my_model.delete()

        # Attempt to retrieve the instance should fail
        with self.assertRaises(MyModel.DoesNotExist):
            MyModel.objects.get(name="Test")

        # Check the cache directly
        cache_key = generate_cache_key(MyModel, name="Test")
        cached_instance = cache.get(cache_key)
        logger.debug(f"Cache Key: {cache_key}, Cached Instance: {cached_instance}")
        self.assertIsNone(cached_instance)

    def test_related_model_cache(self):
        # Create an instance of MyModel
        my_model = MyModel.objects.create(name="Test", description="This is a test.")

        # Create an instance of RelatedModel
        related_model = RelatedModel.objects.create(my_model=my_model, name="Related Test")

        # Retrieve the related instance to ensure it's cached
        retrieved_related_instance = RelatedModel.objects.get(name="Related Test")
        self.assertEqual(retrieved_related_instance.my_model.name, "Test")

        # Check the cache directly
        cache_key = generate_cache_key(RelatedModel, name="Related Test")
        cached_related_instance = cache.get(cache_key)
        logger.debug(f"Cache Key: {cache_key}, Cached Related Instance: {cached_related_instance}")
        self.assertIsNotNone(cached_related_instance)
        self.assertEqual(cached_related_instance.my_model.name, "Test")

