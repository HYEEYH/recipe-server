
# 6월 16일

##### <<  설치한 라이브러리 확인 >> #####
# lamda_app 가상환경
# 파이썬버전 - 3.10

# 설치 라이브러리 : 
# flask , flask-restful, email-validator, 
# psycopg2-binary, passlib, Flask-JWT-Extended
##### --------------------------- #####


# 라이브러리 임포트 -------
from flask import Flask
from flask_restful import Api
from resources.recipe import MyRecipeListResource, RecipeListResource, RecipePublishResource, RecipeRecource
from resources.user import UserLoginResource, UserLogoutResource, UserRegisterResource, jwt_blocklist
from flask_jwt_extended import JWTManager

from config import Config
# -------------------------


### 사용 규칙 : 기본 형식
app = Flask(__name__)

### 환경변수 세팅 - JWT 적용
app.config.from_object(Config)

### JWT 매니저 초기화
# flask프레임워크(app)를 가지고 jwt매니저 적용해라 
jwt = JWTManager(app)

### 로그아웃된 토큰으로 요청하는 경우 -->> 이건 는 비정상적인 접근.
### jwt가 알아서 처리하도록 코드 작성.
# 함수 이름 정해져있음
@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload) :
    jti = jwt_payload['jti']
    return jti in jwt_blocklist





api = Api(app)

# 경로와 API 동작코드(Resource)를 연결한다.
# resource 폴더 만들기 - recipe.py 파일 만들기
	              #   처리함수        ,  '경로'
api.add_resource( RecipeListResource , '/recipes')
		# 경로로 오는 것을 함수로 처리해라
api.add_resource( RecipeRecource , '/recipes/<int:recipe_id>')
        # recipes/<int:recipe_id> 레시피스 뒤에 숫자 오면 처리해달라
api.add_resource( UserRegisterResource  , '/user/register')
        # 회원가입 API
        # 클래스 이름을 이제 지어줘야 함.
        # 클래스이름에는 리소스라고 들어가야 다른사람들이 리소스를 상속받아
        # 쓰는거라고 이해 할 수 있음.
api.add_resource( UserLoginResource  , '/user/login') # 로그인API
api.add_resource( UserLogoutResource  , '/user/logout') # 로그아웃API
api.add_resource(  RecipePublishResource , '/recipes/<int:recipe_id>/publish') 
        # 레시피 공개API
api.add_resource(  MyRecipeListResource  , '/recipes/me')
        # 내 레시피 리스트만 가져오기



if __name__ == '__main__' :
    app.run




# 터미널에 실행 명령어 입력해도 에러만 뜨고 실행이 안 될 경우에는 -->
# 중요!) 항상 저장한 뒤 실행해야 오류가 안난다!

