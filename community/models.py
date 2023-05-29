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
	# front에서 게시물 전체 list 개수 다 보여주고자 할 때 필요해서 추가 정의
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
		default      = 'free', # 게시글 업로드 시 지정하지 않으면 자유토크로
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
	# 1(community):N(comment) 관계니까 Foreign key로 설정
	community  = models.ForeignKey(
				# 'post.Post',
				# verbose_name = 'posts',
				Community, # Community 이미 정의되어 있으니 그냥 바로 객체 가져오도록 수정
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