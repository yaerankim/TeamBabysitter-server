from django.db import models
from user_api.models import User

class Community(models.Model):
	POST_STATUSES = (
			('A', 'Activated'),
			('D', 'Deactivated')
			)

	user    = models.ForeignKey(
	            # 'user_api.User',
	            # related_name = 'users',
				User,
				default      = 1,
	            on_delete    = models.CASCADE,
	        )
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
	row_count = models.IntegerField(
				verbose_name = 'row count',
				default      = 0, 
			)
	# 추천글 선별 위한 좋아요 개수 담을 변수
	like_count = models.IntegerField(
			verbose_name = 'like count',
			default      = 0, 
		)
	comments_count = models.IntegerField(
		verbose_name = 'comments count',
		default      = 0, 
	)
	# 자유토크(free), 질문답변(question) 카테고리
	category = models.CharField(
		verbose_name = 'category',
		default      = 'free',
		max_length = 10,
	)

	class Meta:
		db_table = 'communities'

# 댓글 관련 모델
class Comment(models.Model):
	user       = models.ForeignKey(
	            # 'user_api.User',
	            # verbose_name = 'users',
				User,
				default      = 1,
	            on_delete    = models.CASCADE
	        )
	community  = models.ForeignKey(
				# 'post.Post',
				# verbose_name = 'posts',
				Community,
				on_delete    = models.CASCADE
			)
	content    = models.CharField(
				verbose_name = 'contents',
				max_length   = 128,
			)
	created_at = models.DateTimeField(
				verbose_name = 'created at',
				auto_now_add = True, 
			)
	updated_at = models.DateTimeField(
				verbose_name = 'updated at',
				auto_now     = True
			)