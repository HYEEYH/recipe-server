
# 라이브러리 -------------

from flask_restful import Resource
from flask import request
import mysql.connector
from mysql.connector import Error
from mysql_connection import get_connection
from flask_jwt_extended import get_jwt_identity, jwt_required

# -----------------------

### API 동작하는 코드를 만들기 위해서는
### class(클래스)를 만들어야 한다.

### class란?
# 비슷한 데이터끼리 모아놓은 것(테이블 같은 느낌)
# 클래스는 변수와 함수로 구성된 묶음
# 테이블과 다른점 : 함수가 있다

## API를 만들기 위해서는
## flask_restful 라이브러리의 Resource 클래스를
## 상속해서 만들어야 한다.
## 파이썬에서 상속은 괄호!


# 틀 : class 클래스이름(상속받을것)


class RecipeListResource(Resource) :

    
    @jwt_required()
    def post(self) :  ###### 레시피 등록 API
        ##### 포스트로 요청한 것을 처리하는 코드작성

        ### 테스트해보기 -------------------
        # print('API 동작') # 리턴이없음. 걍 터미널이 프린트하고 끝.

        ## json 형식으로 작성하기
        ## 서버에 프린트 하고 클라이언트에 응답으로 다음 코드를 리턴
        # return {'result' : 'success'}
        ### --------------------------------

        ## 포스트맨의 포스트-바디에 있는 클라이언트가 보내온 데이터 복붙---
        #         { "name" : "김치찌개", 
        #   "description" : "맛있게 끓이는 방법",
        #   "num_of_servings" : 4, 
        #   "cook_time" : 30,
        #   "direction" : "고기 볶고 김치 넣고 물 붓고 두부넣고",
        #   "is_publish" : 1 }
        # ------------------------------------------------------------



        ### 1. 클라이언트가 보낸 데이터를 받아온다.
        # 터미널에 위 클라이언트가 보내온 데이터가 뜨는지 확인
        data = request.get_json()
        print('보내온데이터 확인', data)

        ### 1-1. 헤더에 담긴 JWT 토큰을 받아온다.
        user_id = get_jwt_identity()
        print('토큰확인', user_id)



        ### 2. 받아온 데이터를 DB에 저장한다.
        ### 저장하기 위한 라이브러리 설치
        # $ pip install mysql-connector-python
        ## 라이브러리 임포트---------
        # import mysql.connector
        # -------------------------
        ## config.py 파일 만들어서 데이터베이스 관련 정보 저장.
        ## mysql_connection.py파일 만들기
        # config.py 파일은 깃 이그노어 에 이름을 추가해서 깃허브에 안올라가도록 처리


        ### 2-1. 데이터베이스를 연결한다
        # 라이브러리 임포트 from mysql.connector import Error
        try :
            ### 1) 데이터베이스 연결
            # - 임포트 from mysql_connection import get_connection
            connection = get_connection()

            ### 2) 쿼리문 만든다
            # - mySQL 워크벤치 레시피 디비의 레시피 테이블에서 먼저 쿼리문 작성
	        # - 잘 실행되는지 보고 인서트 내용을 복사 : 실행이 되어야 한다.
	        # - 파이썬으로 돌아와서 복붙
            # query = '''  insert into recipe
            #             (name, description, num_of_servings, cook_time, directions, is_publish)
            #             values
            #             ('볶음밥', '꼬들꼬들 볶음밥 만드는법', 3, 20, '맛있게 잘~', 0 );  '''
            
            ##### 중요!! 컬럼과 매칭되는 데이터만 %s로 바꿔준다!!!  #####
            query = '''insert into recipe
                        (name, description, num_of_servings, cook_time, directions, is_publish, user_id)
                        values
                        (%s, %s, %s, %s, %s, %s, %s );'''
            
            ### 3) 쿼리에 매칭되는 변수처리 - 중요!! 튜플로 처리해준다!
            # - 유저가 입력하는 내용은 포스트맨에 있음(post 리퀘스트부분)
            record = ( data['name'], data['description'],
                      data['num_of_servings'], data['cook_time'],
                      data['directions'], data['is_publish'],
                      user_id)
            
            ### 4) 커서를 가져온다.
            # - 
            cursor = connection.cursor()

            ### 5) 쿼리문을 커서로 실행한다
            cursor.execute(query, record)

            ### 6) DB에 반영완료하라는 commit 해줘야 한다
            connection.commit()

            ### 7) 자원해제
            cursor.close()
            connection.close()



        except Error as e :   # try 안에서 에러나면 이렇게 처리해
            print(e)
            return { 'result' : 'fail', 'error' : str(e) }, 500
            # 500 은 http 상태코드 - 내가 찾아서 넣은 에러 코드



        ### 3. 에러났다면 -> 에러 났다고 알려주고
        ###    그렇지 않으면 -> 잘 저장되었다 알려주기
        return {'result' : 'success'}






    
    def get(self) : ###### 레시피 가져오는 API

        ### get으로 요청한 것을 처리하는 코드 작성
        # print('레시피 가져오는 API -> 동작했음')
        # return { 'result' : 'success', 'count' : 3 }, 400
    

        ### 1. 클라이언트로부터 데이터를 받아온다
        ### 2. 저장된 레시피 리스트를 DB로 부터 가져온다
        ### 3. 데이터 가공이 필요하면 가공한 후 
        ###     클라이이언트에 응답한다.



        ### 1. 클라이언트로부터 데이터를 받아온다
        # -->> 없음


        ### 2. 저장된 레시피 리스트를 DB로 부터 가져온다

        ### 2-1. DB 커넥션

        try : 

            connection = get_connection()

        ### 2-2. 쿼리문을 만든다
            #(수정전)
            # query = '''select *
            #             from recipe
            #             order by created_at desc; '''
            
            # 발행된 레시피만 가져온다(임시저장된건 뺌)
            query = '''select r.* , u.username
                    from recipe r
                    join user u
                    on r.user_id = u.id
                    where is_publish = 1'''

        ### 2-3. 변수 처리할 부분은 변수처리한다.
        ### -->> 없음

        ### 2-4. 커서 가져온다
            cursor = connection.cursor(dictionary= True)

        ### 2-5. 쿼리문을 커서로 실행한다.
            cursor.execute(query)

        ### 2-6. 실행 결과를 가져온다.
            result_list = cursor.fetchall()

            print(result_list) 
            # 프린트 해서 터미널에 나온 결과는 JSON이 아님. XML도 아님.
            # 딕셔너리와 리스트의 조합처럼 생긴게 JSON인데 터미널에 뜬 내용은 전혀 형태 다름
            # JSON의 형태로 변환해야함.
            # cursor라이브러리로 변환할 수 있음
            # cursor = connection.cursor() 의 괄호 안에
            # cursor = connection.cursor(dictionary= True) 이렇게 써주면
            # 가져올때 알아서 JSON 형태로 가져옴.
            # 인터넷에 제이슨에디터 처서 변환하면 됨.

            cursor.close()
            connection.close()

        except Error as e :
            print(e)
            return { 'result' : 'fail', 'error' : str(e)}, 500




        ### 3. 데이터 가공이 필요하면 가공한 후 
        ###     클라이이언트에 응답한다.
        # - 데이터 가공하기 
        # - JSON 으로 변환할때 daytime 형식때문에 자꾸 오류가 남.
        # - created_at, updated_at의 형식을 문자열 형식으로 바꿔줘야함.

        i = 0
        for row in result_list :
            # print(row) # 서버 내렸다가 다시 돌리고 포스트맨에서 send눌러봄 -> row는 딕셔너리
            result_list[i]['created_at'] = row['created_at'].isoformat()
            result_list[i]['updated_at'] = row['updated_at'].isoformat()
            i = i + 1



        # - 에러 안났을때 코드
        return { 'result' : 'success', 
                'count' : len(result_list),
                 'items' : result_list }, 200  # 200은 안써도 됨.





# ===================================================================

class RecipeRecource(Resource) :

    ### GET 메소드에서, 경로로 넘어오는 변수는 get함수의 파라미터로 사용한다
    # def get(self, recipe_id)
    # 메인 파일에서 적힌 함수에서 :
    # api.add_resource( RecipeRecource , '/recipes/<int:recipe_id>') 에서 쓴
    # recipe_id 와 파라미터는 같아야 함.
    


    def get(self, recipe_id) : ###### 특정 레시피 1개 가져오기 API

        # 내가 정의하는 함수 이름이 아니라 정해진 규칙임.
        # print(recipe_id)
        # print(type(recipe_id))
        # recipe_id 의 기본 정보 확인

        ### << 과정 >>> 
        ### 1. 클라이언트로부터 데이터를 받아온다
        ### 2. 데이터베이스에 레시피 아이디로 쿼리한다.
        ### 3. 결과를 클라이언트에 응답한다.
        
        
        ### 1. 클라이언트로부터 데이터를 받아온다
        ### -->> 위의 recipe_id 에 담겨있다

        ### 2. 데이터베이스에 레시피 아이디로 쿼리한다.
        try :
            connection = get_connection()
            # select *
            # from recipe
            # where id = 1;

            #(수정 전)
            # query = ''' select * from recipe
            #         where id = %s; '''
            # 컬럼과 대응되는 값을 쓸때는 %s로 쓸 수 있음
            # recipe_id = %s 로 쓸 수 있다

            # (수정 후)
            # 로그인 한사람, 안한사람 둘 다 볼 수 있다
            # 유저 아이디 안보이게 하기 -> 이름 보이게 하기
            # 임시저장 자기에게만 보이게 하기 -> 1인것만 가져오기
            query = '''select r.* , u.username
                    from recipe r
                    join user u 
                        on r.user_id = u.id
                    where r.id = %s'''

            record = (recipe_id, ) 
                # !!레코드는 항상 튜플로 들어가야함. 
                # 그냥 하나만 쓰면 정수가 됨. 콤마 꼭 필요.!!
            cursor = connection.cursor(dictionary= True)
            cursor.execute(query, record)
            result_list = cursor.fetchall() # 실행한 결과 다 가져와 : 리스트로 옴.
            print(result_list)

            cursor.close()
            connection.close()

        except Error as e: # try부분에서 문제가 발생하면 여기서 처리.
            print(e)
            return {'result' : 'fail', 'error': str(e)}, 500



        ### 3. 데이터가공이 필요하면 가공한 후, 
        ###     결과를 클라이언트에 응답한다.

        i = 0
        for row in result_list :
            # print(row) # 서버 내렸다가 다시 돌리고 포스트맨에서 send눌러봄 -> row는 딕셔너리
            result_list[i]['created_at'] = row['created_at'].isoformat()
            result_list[i]['updated_at'] = row['updated_at'].isoformat()
            i = i + 1

        if len(result_list) != 1 :
            return { 'result': 'success', 'item': {}  }
        else :
            return { 'result': 'success', 'item': result_list[0]}


        # return { 'result': 'success', 'item': result_list[0]}
        # 데이터가 하나이므로 굳이 중괄호 쓸 필요 없어서 result_list[0]
        # 그런데 recipe_id 가 100이 넘어가면 오류남 - 100번째 아이디가 없어서 나오는 오류
        # 빈 딕셔너리 리턴하면 됨. -->> if 함수 추가


        




    @jwt_required()
    def put(self, recipe_id):  ###### 특정 레시피 수정하는 API
        
        ### 1. 클라이언트로부터 데이터 받아오기
        print(recipe_id)

        ### postman의 put 리퀘스트의 body 에 있는 json 데이터를 받아오기
        data = request.get_json()
        print(data)
        
        ### 1-1. user_id 받아온다
        user_id = get_jwt_identity()


        ### 2. 데이터베이스에 업데이트한다.
        try : 
            connection = get_connection()
            query = '''update recipe
                        set name = %s, description = %s,
                            num_of_servings = %s , cook_time = %s, 
                            directions = %s,
                            is_publish = %s
                        where id = %s and user_id = %s;'''

            record = ( data['name'], data['description'], 
                      data['num_of_servings'], data['cook_time'],
                        data['directions'], data['is_publish'],
                        recipe_id , user_id)
            
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()
            cursor.close()
            connection.close()




        except Error as e:
            print(e)
            return { 'result':'fail', 'error':str(e)}, 500
        
        return {'result' : 'success'}







    
    @jwt_required()
    def delete(self, recipe_id) :  ###### 특정 레시피 삭제하는 API
        
        ### 1. 클라이언트로부터 데이터 받아온다.
        ### 2. DB에서 삭제한다
        ### 3. 결과를 응답한다


        ### 1. 클라이언트로부터 데이터 받아온다.
        print(recipe_id)

        user_id = get_jwt_identity()



        ### 2. DB에서 삭제한다
        try : 
            connection = get_connection()
            query = '''delete from recipe
                        where id = %s and user_id = %s;'''
            record = (recipe_id, user_id )
            cursor = connection.cursor()
            cursor.execute(query, record)
            connection.commit()

            cursor.close()
            connection.close()

        except Error as e:
            print(e)
            return {'result':'fail', 'error':str(e)}



        ### 3. 결과를 응답한다
        
        return {'result' : 'success'}




