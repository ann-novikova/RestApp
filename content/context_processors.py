from .models import RestaurantInfo

def restaurant_info(request):
    info = RestaurantInfo.objects.first()
    return {
        'info': info
    }