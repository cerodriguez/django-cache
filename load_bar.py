from bar.models import Bar

# Create instances
Bar.objects.create(name="bar1", is_active=True)
Bar.objects.create(name="bar2", is_active=False)

# Query the model
active_bars = Bar.objects.all()
for bar in active_bars:
    print(f"{bar.name} - {bar.is_active}")  # Should only print bars with is_active=True

