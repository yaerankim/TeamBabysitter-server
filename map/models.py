from django.db import models

# Create your models here.
class Place(models.Model):
    name = models.CharField(
        verbose_name = 'name',
        max_length   = 64,
    )
    address = models.CharField(
        verbose_name = 'address',
        max_length   = 64,
    )
    # 마커 클릭 시 해당 장소의 대표사진으로 보일 이미지 지정
    # image = models.ImageField()

    class Meta:
        db_table = 'places'

class PlaceBabyInfo(models.Model):
    # Place OneToOne 관계로 설정. Place 1: PlaceBabyInfo 1
    place = models.OneToOneField(Place)
    # 정보 취득이 안 된 경우를 생각하여 null을 허용하므로 NullBooleanField 사용
    ramp = models.NullBooleanField(default=False)
    baby_dish = models.NullBooleanField(default=False)
    baby_chair = models.NullBooleanField(default=False)
    nursing_room = models.NullBooleanField(default=False)
    kids_room = models.NullBooleanField(default=False)
    auto_door = models.NullBooleanField(default=False)

# community 모델 대부분 참고
class Review(models.Model):
    POST_STATUSES = (
            ('A', 'Activated'),
            ('D', 'Deactivated')
            )

    # User 제대로 작동 안 하니 일단 주석 처리
    # user    = models.ForeignKey(
    #             'user.User',
    #             related_name = 'users',
    #             on_delete    = models.CASCADE,
    #         )

    # 1(Place):N(Review)
    # Place를 FK로 설정
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    # 각각 기본적인 필드 정의.
    status  = models.CharField(
                verbose_name = 'status',
                choices      = POST_STATUSES,
                default      = 'A',
                max_length   = 1,
            )
    title   = models.CharField(
                verbose_name = 'title',
                max_length   = 64,
            )
    content = models.CharField(
                verbose_name = 'content',
                max_length   = 2000,
            )

    view_count = models.IntegerField(
                verbose_name = 'view count',
                default      = 0, 
            )
    created_at = models.DateTimeField(
                verbose_name = 'created at',
                auto_now_add = True,
            )
    updated_at = models.DateTimeField(
                verbose_name = 'updated at',
                auto_now     = True
            )

    class Meta:
        db_table = 'reviews'