from flask import Flask, render_template,request
import psycopg2
import psycopg2.extras
import os

# FlaskとPostgreSQLを使ったToDoアプリケーション

# app という名前でFlask アプリケーションを作成
app = Flask(__name__)
db_url = os.environ.get("DATABASE_URL")

# データベース接続
def get_db():
    # PostgreSQLデータベースに接続
    # conn = psycopg2.connect(
    #     host=os.environ.get('DATABASE_URL'),
    #     database="todo-postgre",
    #     user="shinmatsumura",
    #     password="password",  # 実際のパスワードに置き換えてください
    #     port=5432
    # )
    conn = psycopg2.connect(db_url, sslmode='require')
    return conn

# def get_db():
#     db = conn.connect(host="127.0.0.1", user="root", port=3306, database="todo_practice2_mysql")
#     db.row_factory = sqlite3.Row
#     return db

# HTMLテンプレートのルートを定義
@app.route('/', methods=['GET'])
def index():
    # tasksのSQL文
    query_tasks = """
        SELECT id,text,user_id
        FROM tasks
    """
    # usersのSQL文
    query_users = """
        SELECT id,name
        FROM users
    """
    # user_idを取得
    user_id = request.args.get('user_id') 
    
    if user_id:
        query_tasks += f" WHERE user_id ={user_id}"
   
    ## データベースに接続
    db = get_db()
    with db:
        # cursor = db.cursor()
        cursor = db.cursor(cursor_factory=psycopg2.extras.DictCursor)

        # SQL文を実行
        cursor.execute(query_tasks)
        ## 取得したデータをtaksksに格納
        tasks = cursor.fetchall()
        # SQL文を実行
        cursor.execute(query_users)
        ## 取得したデータをusersに格納
        users = cursor.fetchall()

    # データベースを閉じる
    # db.close()
    # HTMLにデータを渡して表示
    return render_template('index.html', tasks=tasks, users=users)







