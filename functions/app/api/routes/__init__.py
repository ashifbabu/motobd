"""
Route handlers for the Bangla Motorcycle Review API.
"""

from .bikes import router as bikes_router
from .reviews import router as reviews_router
from .auth import router as auth_router
from .brands import router as brands_router
from .types import router as types_router
from .resources import router as resources_router

# Export routers
bikes = bikes_router
reviews = reviews_router
auth = auth_router
brands = brands_router
types = types_router
resources = resources_router

# Note: Other routers (brands, types, resources) will be added later
__all__ = ['bikes', 'reviews', 'auth', 'brands', 'types', 'resources'] 