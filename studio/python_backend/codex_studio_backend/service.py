from __future__ import annotations
from dataclasses import asdict
from typing import Iterable

class StudioService:
    """Stable Studio-facing contract. GUI clients should call this service only."""

    def __init__(self, engine_adapter):
        self.engine_adapter = engine_adapter

    def discover(self, request):
        return self.engine_adapter.discover(request)

    def validate(self):
        return self.engine_adapter.validate()

    def regress(self):
        return self.engine_adapter.regress()

    def plugins(self):
        return self.engine_adapter.plugins()

    def languages(self):
        return self.engine_adapter.languages()
