class BaseRepository:
    model = None

    def get(self, **kwargs):
        """Retrieve a single object based on filter criteria."""
        try:
            return self.model.objects.get(**kwargs)
        except self.model.DoesNotExist:
            return None

    def filter(self, **kwargs):
        """Retrieve objects that match the filter criteria."""
        return self.model.objects.filter(**kwargs)

    def all(self):
        """Retrieve all objects."""
        return self.model.objects.all()

    def create(self, **kwargs):
        """Create a new object."""
        return self.model.objects.create(**kwargs)

    def update(self, instance, **kwargs):
        """Update an existing object."""
        for field, value in kwargs.items():
            setattr(instance, field, value)
        instance.save()
        return instance

    def delete(self, instance):
        """Delete an object."""
        instance.delete()

    def update_or_create(self, defaults=None, **kwargs):
        """Update an object if it exists, or create it otherwise."""
        defaults = defaults or {}
        return self.model.objects.update_or_create(defaults=defaults, **kwargs)
