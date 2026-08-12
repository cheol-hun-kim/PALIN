import sys
sys.path.append('.')
from app.ai import ask_ai_chatbot

print("--- AI Chatbot Test Output ---")
print(ask_ai_chatbot("안녕 오늘 공부하기 너무 힘들고 지친다 ㅠㅠ"))
