
# 6월 16일

# 라이브러리 임포트 -------
from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource, RecipeRecource
# -------------------------


### 사용 규칙 : 기본 형식
app = Flask(__name__)

api = Api(app)

# 경로와 API 동작코드(Resource)를 연결한다.
# resource 폴더 만들기 - recipe.py 파일 만들기
	              #   처리함수        ,  '경로'
api.add_resource( RecipeListResource , '/recipes')
		# 경로로 오는 것을 함수로 처리해라
api.add_resource( RecipeRecource , '/recipes/<int:recipe_id>')
        # recipes/<int:recipe_id> 레시피스 뒤에 숫자 오면 처리해달라


if __name__ == '__main__' :
    app.run



# 터미널에 실행 명령어 입력해도 에러만 뜨고 실행이 안 될 경우에는 -->
# 중요!) 항상 저장한 뒤 실행해야 오류가 안난다!