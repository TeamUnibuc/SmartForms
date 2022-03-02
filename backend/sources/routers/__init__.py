import routers.form_router as form_router
import routers.entry_router as entry_router
import routers.inference_router as inference_router
import routers.user_router as user_router
import routers.statistics_router as statistics_router

# list of all implemented routers
routers = [
    form_router.router,
    entry_router.router,
    inference_router.router,
    user_router.router,
    statistics_router.router,
]