import sqlite3
from flask_session import Session
import validators
from password_strength import PasswordPolicy, PasswordStats
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, redirect, request, session, jsonify, flash
from anytree import Node, search

# INITIATING FLASK APPLICATION
app = Flask(__name__)

cc = -1

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# CONNECTING TO DATABASE AND CREATING CURSOR OBJECT
# conn = sqlite3.connect("data.db")
conn = sqlite3.connect("connnew.db", check_same_thread=False)
cursor = conn.cursor()


policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=1,  # need min. 1 uppercase letters
    numbers=1,  # need min. 3 digits
    special=1,
      # need min. 1 special characters
)

# CREATING TABLES TO STORE DATA ,AND MAKING SURE NOT TO RECREATE THE TABLES
# with conn:
#     cur.execute(
#         """CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 user TEXT NOT NULL,
#                 master_hash TEXT NOT NULL,
#                 insta TEXT NOT NULL
#     )"""
#     )

class details:
    #To enter values into details table
    def into_values(self,name,passwd,q,insta,fb,tweet):
        id_=self.id_generator(insta)
        if fb==tweet==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}",NULL,NULL);"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta)
        elif fb==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}",NULL,"{tweet}");"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,tweet=tweet)
        elif tweet==None:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}","{fb}",NULL);"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,fb=fb)
        else:
            string="""INSERT INTO details VALUES(
                "{id_}","{passwd}","{name}","{q}","{insta}","{fb}","{tweet}");"""
            sql=string.format(id_=id_,passwd=passwd,name=name,q=q,insta=insta,fb=fb,tweet=tweet)
        cursor.execute(sql)
        return id
    #to get values from details table with id
    def get_value(self,id_):
        cursor.execute("""SELECT id,name,qualification,insta,fb,tweet FROM details WHERE (id="{id_}");""".format(id_=id_))
        data=cursor.fetchall()
        return data
    #To generate or get id for insta
    def id_generator(self,insta):
        cursor.execute("""SELECT id FROM id_detail WHERE (insta="{insta}");""".format(insta=insta))
        z=cursor.fetchall()
        x=[]
        if(z==[]):
            cursor.execute("SELECT * FROM y")
            y=cursor.fetchall()
            yy=y[0]
            x.append(str(hex(yy[0])))
            yy=list(yy)
            yy[0]-=1
            cursor.execute("""INSERT INTO id_detail VALUES("{insta}","{x}");""".format(insta=insta,x=x[0]))
            cursor.execute("UPDATE y SET value={a} WHERE value={b}".format(a=yy[0],b=yy[0]+1))
        else:
            x=z[0]
        return x[0]
    #to store contacts
    def into_contact(self,u_insta,c_insta):
        c_list=[]
        k=0
        id_=self.id_generator(u_insta)
        for j in c_insta:
            c_list.append(self.id_generator(j))
            k+=1
        if k!=20:
            while(k!=20):
                c_list.append(None)
                k+=1
        string="""INSERT INTO contacts VALUES("{id_}","{a}","{b}","{c}","{d}","{e}","{f}","{i}","{j}"
                  ,"{k}","{l}","{m}","{n}","{o}","{p}","{q}","{r}","{s}","{t}","{u}","{v}");"""
        cursor.execute(string.format(id_=id_,a=c_list[0],b=c_list[1],c=c_list[2],d=c_list[3],e=c_list[4],f=c_list[5],i=c_list[6],j=c_list[7],k=c_list[8],l=c_list[9],
        m=c_list[10],n=c_list[11],o=c_list[12],p=c_list[13],q=c_list[14],r=c_list[15],s=c_list[16],t=c_list[17],u=c_list[18],v=c_list[19]))
        return 1
    #To find the contacts from person 1 to person 2
    def find_contact(self,id_2,id_1,c):
        child=[]
        child.append(Node(id_2))
        count=1
        check=[id_2]
        #print("check: ",check)
        note=0
        i=0
        l=0
        print(f"id1: {id_1}, id2: {id_2}")
        while note<=c:
            cursor.execute("""SELECT id FROM contacts WHERE (c1="{id2}" OR c2="{id2}" OR c3="{id2}" OR
                          c4="{id2}" OR c5="{id2}" OR c6="{id2}" OR c7="{id2}" OR c8="{id2}" OR
                          c9="{id2}" OR c10="{id2}" OR c11="{id2}" OR c12="{id2}" OR c13="{id2}" OR
                          c14="{id2}" OR c15="{id2}" OR c16="{id2}" OR c17="{id2}" OR c18="{id2}" OR
                          c19="{id2}" OR c20="{id2}");""".format(id2=check[l]))
            l+=1
            x=cursor.fetchall()
            #for j in x:
            #    print("----",j)
            for j in x:
                if j[0] in check:
                    list(x).remove(j)
            for j in x:
                check.append(j[0])
            if id_1 in check:
                note+=1
                if(note<c+1):
                    for j in x:
                        if(j[0]==id_1):
                            x.remove(j)
                    check.remove(id_1)
            for j in x:
                child.append(Node(j[0],parent=child[i]))
            count+=1
            i+=1
            #print("check: ",check)
            # print(RenderTree(child[0]))

        k=str(search.findall(child[0],filter_=lambda node: node.name in (id_1))).split("/")
        result=[]
        for i in range(1,len(k)-1):
            result.append(k[i])
        g=k[len(k)-1]
        h=len(k[1])
        result.append(g[:h])
        return result
    def times(self,id_1,id_2):
        global cc
        cc+=1
        print("cc: ", cc)
        return self.find_contact(id_1,id_2,cc)

d = details()

@app.route("/")
def landingPage():
    return redirect("/register")

@app.route("/search")
def Search():
    return render_template()


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register User"""

    # IF METHOD IS POST
    if request.method == "POST":

        # RETRIEVING THE DETAILS GIVEN BY THE USER
        username = request.form.get("username")
        insta = request.form.get("insta")
        qualification = request.form.get("qualification")
        password = request.form.get("password")
        stats = PasswordStats(password)
        print("stats:" ,stats.strength())
        # if stats.strength() < 0.66:
        if stats.strength() < 0.4:
            flash("Password not strong enough")
            return redirect("/register")
        rpassword = request.form.get("rpassword")

        # CHECKING TO MAKE SURE THE USER ENTERED VALID DATA
        if not username or not insta or not password or not rpassword:
            return render_template("error.html")

        # GETTING MATCHES FOR THE USER NAME TYPED IN TO EXPEL REDUNDANT USERNAMES
        cursor.execute(
            "SELECT name FROM details WHERE ? IN(SELECT name FROM details)", (username,)
        )
        username_check = cursor.fetchall()
        if len(username_check) > 0:
            return render_template("error.html")
            # return render_template("error.html", "Username already exists!")

        if not password == rpassword:
            return render_template("error.html")
            # return render_template("error.html", "Password Mismatch")

        # IF ALL IS WELL
        if password == rpassword:
            # GENERATE HASH OF MASTER PASSWORD
            hash_password = generate_password_hash(password)

            # INSERT DATA INTO USERS TABLE
            with conn:
                # cur.execute(
                #     "INSERT INTO users (user, master_hash, insta) VALUES (?, ?, ?)",
                #     (username, hash_password, insta),
                # )
                d.into_values(username, hash_password, qualification, insta, None, None)
                # cur.execute("SELECT id FROM users WHERE user=?", (username,))

                id_ = d.id_generator(insta)

            # SET SESSION ID
            session["user_id"] = id_
            return redirect("/home")

    # IF METHOD IS GET
    return render_template("register.html")

ctr = 0

@app.route("/profile_n")
def Profile_n():
    global ctr
    ctr = 0
    return redirect("/profile")

insta = ''

@app.route("/user")
def User():
    data = request.args.get("data")
    print(data)
    return redirect(f"/profile?arg1={data}")


@app.route("/profile", methods=["GET","POST"])
def Profile():
    global ctr
    global cc
    global insta
    ctr += 1
    flag = request.form.get("insta_id")
    if (flag != None):
        insta = flag
    id_inst = d.id_generator(insta)
    print(f"insta: {insta}, insta_id: {id_inst}")
    users_n = []
    if ctr != 1:
        cc -= 1
    try:
        user = d.times(id_inst, session["user_id"])
    except:
        return render_template("error.html")
    users = list(map(d.get_value, user))
    for u in users:
        users_n.append(u[0][3])

    cur_user = request.args.get("arg1")
    print("cur_user: ", cur_user)

    idForDisplay = d.id_generator(cur_user)
    userDetails = d.get_value(idForDisplay)
    print("userdetails: ", list(userDetails))
    username = ''
    job = ''
    instaid = ''
    fbid=''
    for u in users:
        if(u[0][0]==idForDisplay):
            username=u[0][1]
            job = u[0][2]
            instaid = u[0][3]
            fbid=u[0][4]
    print("username: ", username)
    print("job: ",job)
    print("insta id :",instaid)
    print("fb id: ",fbid)

    return render_template("profile.html", users=users_n, username=username,job=job,instaid=instaid,fbid=fbid)

@app.route("/home")
def home():
    if len(session) == 0:
        return render_template("register.html")
    user = cursor.execute("SELECT * FROM details").fetchall()
    if len(user) == 0:
        session.clear()
        return redirect("/register")
    # users = ["user1", "user2", "user3", "user1", "user2", "user3", "user1", "user2", "user3", "user1", "user2", "user3"]
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("error.html")

        username = request.form.get("username")
        password = request.form.get("password")

        # Query database for username
        rows = cursor.execute("SELECT * FROM details WHERE name = ?", (username,)).fetchall()
        # Ensure username exists and password is correct
        print(rows)
        if len(rows) != 1 or not check_password_hash(rows[0][1], password):
            return render_template("error.html")

        # Remember which user has logged in
        session["user_id"] = rows[0][0]

        # Redirect user to home page
        return redirect("/home")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    if len(session) == 0:
        return render_template("register.html")

    # FORGET ANY USER ID
    session.clear()

    # REDIRECT USER TO LOGIN FORM
    return redirect("/login")
