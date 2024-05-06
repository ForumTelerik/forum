import uvicorn
from fastapi import FastAPI
from routers.users import users_router
from routers.categories import categories_router
from routers.topics import topics_router
from routers.admin import admin_router
from routers.replies import replies_router
from routers.votes import votes_router
from routers.messages import messages_router

app = FastAPI()
app.include_router(users_router)
app.include_router(categories_router)
app.include_router(topics_router)
app.include_router(admin_router)
app.include_router(replies_router)
app.include_router(votes_router)
app.include_router(messages_router)

if __name__ == '__main__':
    uvicorn.run('main:app', host='127.0.0.1', port=8000)
'''
Unstuck port in two commands:
netstat -aon | findstr 8000 # gives ProcessID as PID
taskkill /PID 15784 /F      # kills the process
'''