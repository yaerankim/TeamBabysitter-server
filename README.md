# TeamBabysitter-server
* going_baby
  * django 프로젝트의 전체적인 setting 등을 담당
* user_api
  * 로그인, 로그아웃, 회원가입 등의 기능 담당
  * models.py
    * 커스텀 User 모델 정의
  * views.py
    * 현재 회원가입 기능만 작성
    * pw 변수에 대해서 str()은 callable하지 못하다는 error로 제대로 작동X
