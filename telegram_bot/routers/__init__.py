from .order_route import order_router
from .wishlist_route import wishlist_router
from .review_route import review_router
from .review_form_route import review_form_router,review_form_state_router
from .search_route import search_router
from .preference_route import preference_router
from .recommendation_route import recommendation_router
from .static_cmds_route import static_cmds_router
from .error_route import error_router


Routers = [
    order_router,
    wishlist_router,
    review_router,
    review_form_router,
    search_router,
    preference_router,
    recommendation_router,
    static_cmds_router,
    review_form_state_router,
    error_router,
]
