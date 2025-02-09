# How to run this project?
1. apply for a Google Gemini API key first and put it in BabelServer.ini
```aiignore
[Default]
port=8080

[GenAI]
key=PUT YOUR GEMINI KEY HERE
model=gemini-2.0-flash
```
2. run BabelServer.py
```aiignore
python BabelServer.py
```
3. visit https://127.0.0.1:8080/login.html in your web browser
4. input a username and join or create a room, then start your chatting with others!