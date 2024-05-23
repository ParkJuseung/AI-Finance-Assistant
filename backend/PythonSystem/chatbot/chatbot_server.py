
from flask import Flask, request, jsonify
from chatbot_main import ChatEngine
from topic_main import TopicEngine
from datetime import datetime

## 추가_12주차: init ##
chatbot_engine=ChatEngine()
topic_engine=TopicEngine()

## 서버 RUN ##
app = Flask(__name__)

## springboot에서 chatbot 대화 처리 요청 시, 처리 및 응답 메시지 리턴 함수(post 방식) ##
@app.route('/chatbot-message', methods=['POST'])
def chatbot_request_process():
    print(f"\t[Client][Spring-Boot][Request-chatbot][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received Checked!")
    data = request.json # REST API 방식으로, JSON 형식을 사용.
    username = data.get('username') # springboot가 username을 보냈는지 확인(username == 로그인ID)
    text = data.get('text')
    # sk하이닉스와 같이, 소문자 영어가 있는 경우
    if text.islower():
        text=text.upper()

    print(f"\t[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 요청자:spring-boot / 대화고객명:{username}")
    
    # chatbot_main 불러오기 : 수정1_12주차 : 전역변수로 변경
    #engine=ChatEngine()
    
    # 사용자 입력에 맞춰 새로운 레코드 chatbot_history에 삽입
    chatbot_engine.insert_new_record(username, text)
    
    # 사용자 입력에 대한 답변 처리
    flag=chatbot_engine.chatbot_process()
    
    # 처리완료 알림을 spring-boot에 응답.
    if flag:
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response-status: 200\n")
        return jsonify({'state': 'true'}), 200 # 메시지(JSON형식), 상태코드
    else:
        chatbot_engine.update_record_res_msg() # 서버 오류로 인한 답변 불가 처리
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response-status: 400\n")
        return jsonify({'state': 'false'}), 400


## 추가_10주차: springboot에서 관련 뉴스 '토픽 인사이트'버튼 클릭시, 처리 및 응답 메시지 리턴 함수(post 방식) ##
@app.route('/news-insite', methods=['POST'])
def news_topic_insite():
    print(f"\t[Client][Spring-Boot][Request-news_insite][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Received Checked!")
    data = request.json # REST API 방식으로, JSON 형식을 사용.
    title = data.get('title')
    
    print(f"\t\t title={title}")
    
    # topic_main.py 불러오기 : 수정1_12주차 : 전역변수로 변경
    #engine=TopicEngine()
    
    # title에 해당되는 content 얻기.
    text=topic_engine.preprocess(title)
    if text=="":
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] content 발견 못함")
        return jsonify({'state': 'false'}), 400
    
    # content 요약 얻기
    result_summary=topic_engine.run_summary(text)
    
    # content 인사이트 얻기
    result_quest, result_answer = topic_engine.run_insite(text)
    quest_text,answer_text = "",""
    if result_quest!=[] and result_answer!=[]:
        for q,a in zip(result_quest, result_answer):
            quest_text=quest_text+q+"\n"
            answer_text=answer_text+a+"\n"
        
    # 처리 완료
    if result_summary=="" and quest_text=="":
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 요약 에러 처리 / 인사이트 에러 처리")
        return jsonify({'state': 'false'}), 400
    elif result_summary!="" and quest_text=="":
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 요약 존재 / 인사이트 에러 처리")
        return jsonify({
            'summary': result_summary,
            'questions': quest_text,
            'answers': answer_text,
            'state': 'true'
            }), 200
    elif result_summary=="" and quest_text!="":
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 요약 에러 처리 / 인사이트 존재")
        return jsonify({
            'summary': result_summary,
            'questions': quest_text,
            'answers': answer_text,
            'state': 'true'
            }), 200
    else:
        print(f"\t[Server][Flask][Response][{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response-state : 200")
        return jsonify({
            'summary': result_summary,
            'questions': quest_text,
            'answers': answer_text,
            'state': 'true'
            }), 200
    
if __name__ == '__main__':
    #app.run(debug=True) # 개발
    app.run(debug=False) # 운영