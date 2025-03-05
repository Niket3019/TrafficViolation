from django.contrib import admin
from django.apps import apps

# Get all models from the current app
models = apps.get_models()

# Register each model
for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass  # Skip if already registered
