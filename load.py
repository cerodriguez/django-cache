import time

from foo.models import MyModel


# start time
start = time.time()
for i in range(1,1_000_000):
    try :
        my_model = MyModel.objects.get(name="foo")
    except MyModel.DoesNotExist:
        print("Object does not exist")
        my_model = MyModel.objects.create(name="foo", description="bar")
    print(my_model)

# end time
end = time.time()
print(f"Time taken: {end-start}")

# Results:
# no cache 
# Time taken: 96.80815839767456

# with cache
# Time taken: 12.323495864868164

