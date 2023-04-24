from django.db import models

class Community(models.Model):
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
        db_table = 'communities'

# 댓글 관련 모델
# 일단 급하지 않으니 주석 처리
# class Comment(models.Model):
#     user       = models.ForeignKey(
#                 'user.User',
#                 verbose_name = 'users',
#                 on_delete    = models.CASCADE
#             )
#     post       = models.ForeignKey(
#                 'post.Post',
#                 verbose_name = 'posts',
#                 on_delete    = models.CASCADE
#             )
#     content    = models.CharField(
#                 verbose_name = 'contents',
#                 max_length   = 128,
#             )
#     created_at = models.DateTimeField(
#                 verbose_name = 'created at',
#                 auto_now_add = True, 
#             )
#     updated_at = models.DateTimeField(
#                 verbose_name = 'updated at',
#                 auto_now     = True
#             )