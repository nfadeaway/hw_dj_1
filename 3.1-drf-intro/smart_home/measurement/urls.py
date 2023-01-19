from django.urls import path

from measurement.views import SensorsView, SensorDetail, MeasurementsAdd


urlpatterns = [
    path('sensors/', SensorsView.as_view()),
    path('sensors/<pk>/', SensorDetail.as_view()),
    path('measurements/', MeasurementsAdd.as_view()),
]
