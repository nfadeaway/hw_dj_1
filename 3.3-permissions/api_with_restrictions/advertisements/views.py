from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Advertisement, FavoriteAdv
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrReadOnly()]
        return []

    # Фильтруем начальный queryset с доступом к DRAFT объявлениям
    def get_queryset(self):
        return super().get_queryset().exclude(Q(status='DRAFT') & ~Q(creator_id=self.request.user.id))

    # Добавляем в объявление в избранное
    @action(detail=True, methods=['POST'])
    def addtofavorites(self, request, pk=None):
        obj = self.get_object()
        if request.user.id is None:
            return Response('Вы не авторизованы')
        favorites = FavoriteAdv.objects.filter(user_id=request.user.id, favorite_adv=obj.id)
        if favorites:
            return Response('Объявление уже в избранном')
        adv = Advertisement.objects.filter(id=obj.id)
        if request.user.id == adv[0].creator_id:
            return Response('Вы не можете добавить собственное объявление в Избранное')
        else:
            FavoriteAdv.objects.create(favorite_adv=obj.id, user_id=request.user.id)

        return Response(f'Объявление {obj.id} добавлено в Избранное!')

    # Выводим список избранного
    @action(detail=False, methods=['GET'])
    def showmyfavorites(self, request):
        if request.user.id is None:
            return Response('Вы не авторизованы')
        favorites_list = []
        user_favorites = FavoriteAdv.objects.filter(user_id=request.user.id)
        for favorite in user_favorites:
            favorites_list.append(favorite.favorite_adv)
        print(favorites_list)
        result_queryset = Advertisement.objects.filter(id__in=favorites_list)
        serializer = AdvertisementSerializer(result_queryset, many=True)
        return Response(serializer.data)
