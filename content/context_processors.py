from .models import RestaurantInfo


def restaurant_info(request):
    """Контекстный класс для получения инфо о ресторане во всех шаблонах"""

    info = RestaurantInfo.objects.first()
    return {"info": info}
