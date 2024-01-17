## Bearer authentication
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi import FastAPI, HTTPException, status
import datetime
import os
from tortoise.contrib.fastapi import register_tortoise
import jwt
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import HTTPException, status
import time
import json
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse


from authentication import *
from models import *

app = FastAPI(title="Quizapp API", openapi_url="/api/docs/openapi.json", docs_url="/api/docs", redoc_url="/api/redoc")

origins = [ "http://localhost:3000", "http://127.0.0.1:3000",
            "http://localhost:5173", "http://127.0.0.1:5173"
            ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_URL = os.environ.get("DB_URL", "sqlite://db.sqlite3")
JWT_SECRET = os.environ.get("JWT_SECRET", "secretlolol")
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

print(f"Connecting to '{DB_URL}'")
register_tortoise (
    app,
    db_url=DB_URL,  # läuft über lokale sqlite Datenbank, sollte noch in postgres Datenbank ausgelagert werden
    modules={"models": ["main", "models", "authentication"]},
    generate_schemas=True,
    add_exception_handlers=True
)

###########################################
############# USER MANAGEMENT #############
###########################################


@app.post("/api/login", description="Returns a bearer Access Token on successful login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    user_obj = await User_Pydantic.from_tortoise_orm(user)
    tokendump = {
        "id": user_obj.id,
        "sub": user_obj.username,
        "roles": ["user"]#, # TODO: hier kann die "admin" role noch mit rein, sollte halt im user model gespeichert werden
        #"exp": int(time.time() + 3600) # Expires in 1h / 3600 seconds
    }
    #token = jwt.encode(user_obj.model_dump(), JWT_SECRET) # Dadurch ist halt der pw-hash im payload aber naja es wird schon niemand nachsehen, pssst
    token = jwt.encode(tokendump, JWT_SECRET)
    return {"access_token" : token, "token_type" : "bearer"}


@app.post("/api/register", response_model=User_Pydantic, description="Creates a new User with given credentials")
async def register(user: UserIn_Pydantic):
    user_obj = User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


async def get_current_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return await User_Pydantic.from_tortoise_orm(user)


async def is_admin_user(token: str = Depends(oauth_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = await User.get(id=payload.get("id"))
        if not payload.get("id") == 4:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Admin privileges")
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    return await User_Pydantic.from_tortoise_orm(user)


@app.get("/api/user/me", response_model=User_Pydantic, description="Returns user data of logged in user")
async def users_me(user: User_Pydantic = Depends(get_current_user)):
    return user

#################################
############# LOGIC #############
#################################

@app.get("/api/user/quizzes", description="Returns all the Quizes the logged in user created")
async def users_quizes(user: User_Pydantic = Depends(get_current_user)):
    response = []
    try:
        for quiz in await Quiz_Tortoise.filter(creator=user.id).all():
            response.append(quiz)
    except:
        return{"Quizes": []}
    return {"Quizes": response}


@app.post("/api/user/quiz", description="Post Quiz as User")
async def users_quiz(post_quiz: Quiz_Pydantic, user: User_Pydantic = Depends(get_current_user)):
    pre_id = 1
    try:
        tmp = await Quiz_Tortoise.all().order_by('-id').limit(1).values('id')
        pre_id = int(tmp[0]["id"]) + 1
    except Exception as e:
        print(e)
    quiz = Quiz_Tortoise(
        id = pre_id,
        creator = user.id,
        title = post_quiz.title,
        desc = post_quiz.desc,
        category = post_quiz.category,
        created = datetime.datetime.now().date(),
        modified = datetime.datetime.now().date(),
        plays = 0
    )
    await quiz.save()

    for post_question in post_quiz.questions:
        pre_id = 1
        try:
            tmp = await Question_Tortoise.all().order_by('-id').limit(1).values('id')
            pre_id = int(tmp[0]["id"]) + 1
        except Exception as e:
            print(e)
        question = Question_Tortoise(
            id = pre_id,
            quiz_id = quiz.id,
            title = post_question.title,
            answers = json.dumps(post_question.answers),
            points = post_question.points
        )
        await question.save()

    return {"status": "successful", "id": quiz.id}


async def addRating(rating: Rating_Tortoise):
    try:
        existing_rating = await Rating_Tortoise.get(user=rating.user, question=rating.question)
        existing_rating.points = rating.points
        await existing_rating.save()
    except:
        await rating.save()


@app.post("/api/user/check_answer", description="Post answer which is evaluated and returns result. Stores received points.")
async def user_check_answer(answer: Answer_Pydantic, user: User_Pydantic = Depends(get_current_user)):
    tmp_id = 1
    try:
        tmp = await Rating_Tortoise.all().order_by('-id').limit(1).values('id')
        tmp_id = tmp[0]["id"]
    except:
        ...
    rating = Rating_Tortoise(
        id= tmp_id + 1,
        user=user.id,
        question=answer.question,
        points=0
    )
    correct = False
    if answer.chosen == 0: # Antwort 0 ist immer die richtige aktuell lol
        correct = True
        try:
            question = await Question_Tortoise.get(id=answer.question)
            rating.points = question.points
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Question does not exist")
    await addRating(rating)
    return {"output": correct}


@app.get("/api/quizzes", description="Returns all the quizzes")
async def quizzes(user: User_Pydantic = Depends(get_current_user)):
    return {"Quizes": [item for item in await Quiz_Tortoise.all()]}


@app.get("/api/quizzes/ids", description="Returns all the quiz ids")
async def quizzes_ids(user: User_Pydantic = Depends(get_current_user)):
    return {"IDs": [item.id for item in await Quiz_Tortoise.all()]}


@app.get("/api/quizzes/quiz", description="Returns the Quiz with given ID")
async def quizzes_quiz(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    try:
        obj = await Quiz_Tortoise.get(id=quiz_id)
        pydantic_obj = await Quiz_Tortoise_Pydantic.from_tortoise_orm(obj)
        return pydantic_obj
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quiz with given ID")


@app.get("/api/quizzes/quiz/questions", description="Returns all the Questions of given Quiz ID and increases plays counter")
async def quizzes_quiz_questions(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    quiz = await Quiz_Tortoise.get(id=quiz_id)
    quiz.plays += 1
    await quiz.save()
    response = []
    try:
        for question in await Question_Tortoise.filter(quiz_id=quiz_id).all():
            response.append(question)
    except:
        return {"Questions": []}
    return {"Questions": response}


@app.get("/api/quizzes/quiz/bestlist", description = "Returns bestlist for quiz with given id")
async def quizzes_quiz_bestlist(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    try:
        results = {}
        for rating in await Rating_Tortoise.all():
            for question in await Question_Tortoise.filter(quiz_id=quiz_id).all():
                if rating.question == question.id:
                    username = str(rating.user)
                    if not username in results:
                        results[username] = rating.points
                    else:
                        results[username] += rating.points
                    break
        results = sorted(results.items(), key=lambda x: x[1], reverse=True)
        tuples = []
        for result in results:
            tmp_user = await User.get(id=int(result[0]))
            tuples.append( (tmp_user.username, result[1]))
        return tuples
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, description = "Keine Ahnung bruh")


@app.get("/api/quizzes/quiz/bestlist/user", description = "Returns how many points a user has in given Quiz. Returns a percentage")
async def quizzes_quiz_bestlist_user(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    points = -1
    for rating in await Rating_Tortoise.filter(user=user.id):
        question = await Question_Tortoise.get(id=rating.question)
        if quiz_id == question.quiz_id:
            if points == -1:
                points = 0
            points += rating.points
    possible = 0
    for question in await Question_Tortoise.filter(quiz_id=quiz_id):
        possible += question.points
    if possible == 0:
        return {"points_percentage": 0}
    if points == -1:
        return {"points_percentage": -1}
    return {"points_percentage": points/possible}


@app.get("/api/quizzes/quiz/bestlist/user/points", description = "Returns how many points a user has in given Quiz. Returns the absolute number")
async def quizzes_quiz_bestlist_user_points(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    points = -1
    for rating in await Rating_Tortoise.filter(user=user.id):
        question = await Question_Tortoise.get(id=rating.question)
        if quiz_id == question.quiz_id:
            if points == -1:
                points = 0
            points += rating.points
    possible = 0
    for question in await Question_Tortoise.filter(quiz_id=quiz_id):
        possible += question.points
    if possible == 0:
        return {"points": 0, "possible": 0}
    if points == -1:
        return {"points": -1, "possible": -1}
    return {"points": points, "possible": possible}


@app.get("/api/user/landingpageinformation", description = "Returns Information for Display on Landingpage for logged in user")
async def user_landingpageinformation(user: User_Pydantic = Depends(get_current_user)):
    try:
        absolvierte_quizzes = []
        gesammelte_punkte = 0
        for rating in await Rating_Tortoise.all():
            if rating.user == user.id:
                question = await Question_Tortoise.get(id=rating.question)
                if not question.quiz_id in absolvierte_quizzes:
                    absolvierte_quizzes.append(question.quiz_id)
                gesammelte_punkte += rating.points
        erstellte_quizzes = 0
        eigene_quizzes_wurden_gespielt = 0
        for quiz in await Quiz_Tortoise.all():
            if quiz.creator == user.id:
                erstellte_quizzes += 1
                eigene_quizzes_wurden_gespielt += quiz.plays
        return {"played_quizzes": len(absolvierte_quizzes), "collected_points": gesammelte_punkte, "created_quizzes": erstellte_quizzes, "quiz_plays": eigene_quizzes_wurden_gespielt}
    except Exception as e:
        print(e)
        return {"ERROR": -9}


@app.post("/api/delete/user/quiz", description="Deletes the quiz with given ID if logged in user is creator of the Quiz")
async def delete_user_quiz(quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
    try:
        target_quiz = await Quiz_Tortoise.get(id=quiz_id)
        if target_quiz.creator != user.id:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not the creator of the Quiz")
        await target_quiz.delete()
        questions = await Question_Tortoise.filter(quiz_id=quiz_id)
        for question in questions:
            await Rating_Tortoise.filter(question=question.id).delete()
            await question.delete()
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quiz with given ID")


###########################################
############### ADMIN STUFF ###############
###########################################


@app.post("/api/admin/delete_ratings_of_question", description="Deletes the ratings of question with given ID", deprecated=True)
async def admin_delete_ratings_of_question(question_id: int, user: User_Pydantic = Depends(is_admin_user)):
    try:
        await Rating_Tortoise.filter(question=question_id).delete()
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Question with given ID")


@app.post("/api/admin/delete_question", description="Deletes the question with given ID", deprecated=True)
async def admin_delete_question(question_id: int, user: User_Pydantic = Depends(is_admin_user)):
    try:
        question = await Question_Tortoise.get(id=question_id)
        await question.delete()
        await Rating_Tortoise.filter(question=question_id).delete()
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Question with given ID")


@app.post("/api/admin/delete_quiz", description="Deletes the quiz with given ID")
async def admin_delete_quiz(quiz_id: int, user: User_Pydantic = Depends(is_admin_user)):
    try:
        await Quiz_Tortoise.filter(id=quiz_id).delete()
        questions = await Question_Tortoise.filter(quiz_id=quiz_id)
        for question in questions:
            await Rating_Tortoise.filter(question=question.quiz_id).delete()
        await questions.delete()
        return {"status": "success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Quiz with given ID")


@app.get("/api/admin/demorating", description = "Returns demorating")
async def admin_demorating(user: User_Pydantic = Depends(is_admin_user)):
    return [
        ("user15", 100),
        ("user14", 95),
        ("user13", 90),
        ("user12", 85),
        ("user11", 80),
        ("user10", 75),
        ("user9", 70),
        ("user8", 65),
        ("user7", 60),
        ("user6", 55),
        ("user5", 50),
        ("user4", 45),
        ("user3", 40),
        ("user2", 35),
        ("user1", 30)
    ]


@app.get("/api/admin/ratings", description = "Returns all ratings")
async def admin_ratings(user: User_Pydantic = Depends(is_admin_user)):
    return {"Ratings": [item for item in await Rating_Tortoise.all()]}


@app.get("/api/admin/questions", description="Returns all the Questions")
async def admin_questions(user: User_Pydantic = Depends(is_admin_user)):
    return {"Questions": [item for item in await Question_Tortoise.all()]}


###########################################
############## TESTING STUFF ##############
###########################################


###########################################
################## DUMP ###################
###########################################

#@app.post("/api/users/quiz/questions", description="Post Question to given Quiz ID")
#async def post_question(post_question: Question_Pydantic, quiz_id: int, user: User_Pydantic = Depends(get_current_user)):
#    try:
#        existing_quiz = await Quiz_Tortoise.get(id=quiz_id)
#        if not user.id == existing_quiz.creator:
#            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No Permission to edit this Quiz")
#    except:
#        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Requested Quiz does not exist")
#    tmp_id = 1
#    try:
#        tmp = await Question_Tortoise.all().order_by('-id').limit(1).values('id')
#        tmp_id = tmp[0]["id"]
#    except:
#        ...
#    question = Question_Tortoise(
#        id = tmp_id + 1,
#        quiz_id=quiz_id,
#        title=question.title,
#        answers=question.answers,
#        points=question.points
#    )
#    await question.save()
#    return {"status": "successful", "id": question.id}