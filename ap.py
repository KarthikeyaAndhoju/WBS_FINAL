from random import randrange
from typing import Optional
from fastapi import  FastAPI , Response , status, HTTPException,Request,Form
from fastapi.params import Body
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import psycopg2
from psycopg2.extras import RealDictCursor
import re 
#from apis.general_pages.route_homepage import general_pages_router
'''from . import models
from .database import engine, session_local

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()'''



app = FastAPI()
templates = Jinja2Templates(directory="html")
student=[{"name":"vansh","rollno":"556","id":1},{"name":"vanshnawander","rollno":"556","id":2}]
class student_registration(BaseModel):
    fullname: str
    email: str 
    college : str
    domain: str
    year:  str 
    dob : str 
    address : str 
    username: str 
    password: str 
    cpassword: str 
    #section: Optional[str]=None

try:
    conn= psycopg2.connect(host="localhost",database="postgres",user="postgres",password="aarvi3953",cursor_factory=RealDictCursor)
     
    cursor=conn.cursor() 
    print("databasse connected")
except Exception as e:
    print("database failed to connect")
    print("error : ",e)    



def fin(id):
    for i in student:
        if i["id"]==id:
            return i

def del_ind(id):
    for i,j in enumerate(student):
        if j["id"]==id:
            return i
    return 0

app.mount("/static", StaticFiles(directory="html"), name="static")


@app.get("/")
def home(request:Request):
    return templates.TemplateResponse("Signin.html",{"request": request})

@app.post("/submit")
def login_check(request:Request,username:str=Form(...),password:str=Form(...)):
    cursor.execute(""" SELECT * FROM user_regist WHERE username=%s and password=%s""",(username,password))
    a=cursor.fetchone()
    if(a==None):
        return {"invalid user"}
    else:
        return templates.TemplateResponse("index1.html",{"request": request})


@app.get("/vansh")
def page():
    return "vansh"

@app.get("/posts")
async def root():
    return {"message": student}
@app.get("/home")
async def register(request:Request):
    return templates.TemplateResponse("index1.html",{"request": request})

@app.get("/register")
async def register(request:Request):
    return templates.TemplateResponse("Signup.html",{"request": request})
@app.get("/explore")
async def register(request:Request):
    return templates.TemplateResponse("explore.html",{"request": request})
@app.get("/topchoice")
async def register(request:Request):
    return templates.TemplateResponse("chtop.html",{"request": request})
@app.get("/contactus")
async def register(request:Request):
    return templates.TemplateResponse("cus.html",{"request": request})

@app.post("/registration")
def create_post(request:Request ,fullname: str=Form(...),
    email: str =Form(...),
    college : str=Form(...),
    domain: str=Form(...),
    year:  str =Form(...),
    dob : str =Form(...),
    address : str =Form(...),
    username: str =Form(...),
    password: str =Form(...),
    cpassword: str =Form(...)):
    #print(ab.dict())
    #dic["id"]=randrange(0,1000000)
    #student.append(dic)
    l=[check(email),check1(fullname),check2(year)]
    if(len(password)<6 or len(password)>12)  :
        l.append("password length between 6 to 12")
    if(password!=cpassword):
        return {"password didn not match"} 
    
    for i in l:
        if(i==""):
            l.pop(l.index(i))
    if(len(l)>0):
        return l
            
    cursor.execute("""INSERT INTO user_regist(fullname, email,college,domain,dob,address,username,password,year) values(%s,%s,%s,%s,%s,%s,%s,%s,%s) """,(fullname, email,college,domain,dob,address,username,password,year))
    #a=cursor.fetchone()
    conn.commit()
    return templates.TemplateResponse("Signin.html",{"request": request})

@app.get("/posts/{id}")
def get_post(id:int,response : Response):
    print(id)
    a=fin(id)
    if not a:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="the is not found exception try")
        #response.status_code=status.HTTP_404_NOT_FOUND
        #return{"response":"the id not found in data base"}
    return{"data":a}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    x=del_ind(id)
    student.pop(x)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}",status_code=status.HTTP_205_RESET_CONTENT)
def post_update(id :int,ab:student_registration):
    x=del_ind(id)
    abc=ab.dict()
    student[x]["name"]=abc["fullname"]
    student[x]["rollno"]=abc["email"]
    student[x]["section"]=abc["year"]
    return{"message":ab}
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
regex2 = r'\b[A-Za-z_%+-]\b'
# Define a function for
# for validating an Email
regex1 = r'\b[A-Za-z._%+-]\b' 
 
def check(email):
    if(re.fullmatch(regex, email)):
        return ""
    else:
        return "invalid email adderss"
def check1(fullname):
    if(re.fullmatch(regex1, fullname)):
        return ""
    else:
        return "invalid full name"

def check5(address):
    if(re.fullmatch(regex1, address)):
        return ""
    else:
        return "invalid city"


def check2(year):
    try:
        st=int(year)
        abc=len(year)
        if(st<1950 or st>2030):
            return "please enter year between 1950 to 2030"
    except:
        return "invalid year"


