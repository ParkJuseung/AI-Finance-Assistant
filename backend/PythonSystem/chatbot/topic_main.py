"""
관련 뉴스의 기사 토픽 인사이트 Chatgpt 처리 클래스
"""
import pymysql
import pandas as pd
from openai import OpenAI
import time
import re

class TopicEngine:
    def __init__(self):
        self.conn = pymysql.connect(host="127.0.0.1", user="root", password="비밀번호", db="testcapstone", charset="utf8")
    
    def __del__(self):
        self.conn.close()
    
    def preprocess(self,title):
        try:
            with self.conn.cursor() as curs:
                sql="""
                SELECT * FROM news_articles WHERE title=%s
                """
                curs.execute(sql,title)
                result=curs.fetchall()
                df=pd.DataFrame(result)
                df.columns=['code','date','title','content','image','url']
                print(f"\t\trecord_count: {df.shape[0]}")
                if df.shape[0]<1:
                    return ""
                elif df.shape[0]>1:
                    df=df.sort_values(by='date')
                    return df['content'].iloc[-1]
                elif df.shape[0]==1:
                    return df['content'].iloc[-1]
        except:
            print("\t\t[topic_main][preprocess] Error 발생")
            return ""
    
    def run_summary(self, text):
        try:
            messages=[{"role": "system", "content": "You are a helpful assistant."}]
            messages.append({"role":"user", "content": f"""
                            너는 뛰어난 뉴스 분석가의 임무를 맡게 되었어.
                            
                            다음의 뉴스 내용에 대해 요약해줘.
                            
                            '{text}'
                            
                            요약 기준은 다음과 같아.
                            1. 전체 기사 뉴스 내용 요약
                            2. 3가지에서 5가지 핵심 설명
                            
                            너가 나에게 답변(출력)하는 형식을 다음과 같은 예시를 통해 알려줄게.
                            
                            '
                            삼성전자는 금일 컨퍼런스에서 향후 사업 전망에 관한 발표를 진행하였다.
                            
                            1) 삼성전자는 2024년 겔럭시 링을 출시한다는 발표를 하였다.
                            
                            2) 냉장고에 대해, 인공지능 기술을 탑재하여 고객들의 만족도가 급상승하였다.
                            
                            ...(중략)
                            '
                            
                            요약 기준과 답변 형식 예시를 참고해서, 한글로 뉴스 내용을 요약해줘.
                            """})
                
            openai = OpenAI(api_key="")
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages
            )
            result=response.choices[0].message.content
            
            #print("[결과1]")
            #print(result)
            return result
        except:
            print("\t\t[topic_main][run_summary] Error 발생")
            return ""
    
    def run_insite(self, text):
        try:
            result,cnt="",1
            while cnt<=5:
                messages=[{"role": "system", "content": "You are a helpful assistant."}]
                messages.append({"role":"user", "content": f"""
                                너는 뛰어난 뉴스 분석가의 임무를 맡게 되었어.
                                
                                다음의 뉴스 내용에 대해 분석한 후, 3가지의 인사이트 Q&A를 생성해줘.
                                
                                '{text}'
                                
                                너가 나에게 답변(출력)해야하는 출력 형식은 다음과 같은 예시를 통해 알려줄게.
                                
                                '
                                Q1) 냉장고 신제품에 대해 고객들의 만족도가 상승한 이유는 무엇인가?
                                A1) 삼성전자는 냉장고에 인공지능 기술을 융합하여, 냉장고 자동 히팅 시스템으로 인해 고객들의 사용 편의성이 증가한 것으로 분석된다.
                                
                                Q2) 삼성전자의 주가가 상승한 핵심 이유는 무엇인가?
                                A2) 2024년 컨퍼런스에서 갤럭시 링의 출시 발표가 주가에 영향을 미친 것으로 분석된다.
                                
                                Q3) 반도체 수요가 급증한 이유는 무엇인가?
                                A3) 삼성전자는 D랩에 새로운 기술을 적용하여, 반도체 산업의 큰 영향을 미친 것으로 분석된다.
                                '
                                
                                3가지의 인사이트 Q&A를 생성한 후, 예시로 들어준 출력 형식처럼 나에게 보이게끔 답변해줘.
                                """})
                    
                openai = OpenAI(api_key="")
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages
                )
                res=response.choices[0].message.content
                if ('Q' in res and 'A' in res) or ('q' in res and 'a' in res):
                    result=res
                    break
                cnt+=1
                print(f"\t\t인사이트 chatgpt 재요청.. #{cnt}")
                print(f"\t\tres")
                print()
                time.sleep(2)
                
            
            #print("[결과]")
            #print(result)
            
            if result=="":
                print("\t\t[topic_main][run_insite] 5번 요청하였으나, 원하는 답변 못받음 처리")
                return [],[]
            result_filter=result.strip()
            lines = result_filter.split('\n')
            questions = [line.split(') ')[1].strip() for line in lines if line.startswith('Q')]
            answers = [line.split(') ')[1].strip() for line in lines if line.startswith('A')]
            # questions = re.findall(r'Q\d+\) (.+?)(?=Q|\Z)', result_filter)
            # answers = re.findall(r'A\d+\) (.+?)(?=A|Q|\Z)', result_filter)
            #print(questions)
            #print()
            #print(answers)
            return questions, answers
        except:
            print("\t\t[topic_main][run_insite] Error 발생")
            return [],[]
        
