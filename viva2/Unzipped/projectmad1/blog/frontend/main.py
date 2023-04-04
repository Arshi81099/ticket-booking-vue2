import os
from flask import Flask, jsonify, redirect, render_template, request, make_response, session, url_for
import requests
import json


app = Flask(__name__)
app.secret_key = "thisisthesecretkey"


api="http://127.0.0.1:5000"


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    if 'user_id' in session:
        username = session['username']
        return redirect('/feed')
    else:
        return redirect('/login')

@app.route("/feed",methods=["GET","POST"])
def getNewsFeed():
    if "username" in session:
        username = session['username']
        
        following_list = requests.get(f'{api}/follow/{username}')
        posts_feed = requests.get(f'{api}/feed/{username}')
        if following_list.status_code == 200 and posts_feed.status_code == 200:
            follows = following_list.json()
            # print(follows)
            follows = follows[1]

            posts = posts_feed.json()
            # print(len(posts))
            # post = posts[2]
            # print(post['username'])
            return render_template('feed.html', username=username, posts=posts, follows=follows)

        else:
            return "OOPS!!"
    else:
        return redirect('/login')

@app.route("/mypost",methods=["GET","POST"])
def mypost():
    if "username" in session:
        username = session['username']
        posts_feed = requests.get(f'{api}/userpost/{username}')
        if posts_feed.status_code == 200:
            posts = posts_feed.json()
            # print(posts)
            return render_template('mypost.html', username=username, posts=posts)
        else:
            return "OOPS!!"
    else:
        return redirect('/login')

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']


        x = requests.get(f'{api}/user/{username}')

        if x.status_code == 200:
            response = x.json()
            # print(response)
            user_pass = response['password']

            if user_pass == password:
                session['username'] = response['username']

                return redirect('/feed')
            else:
                return 'Invalid username or password'
        else:
            return render_template("register.html")
    else:
        return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():
    if request.method == "POST":
        form = request.form
        username = form["username"]
        name = form["name"]
        password = form["password"]
        email= form["email"]
        confirm_password = form["confirmPassword"]
        print(username)
        if confirm_password != password:
            return redirect('/register')

        data = {
	"username":username,
	"name":name,
	"email":email,
	"password":password
}

        x = requests.post(f"{api}/user", json=data)
        # print(x.text)
        if x.status_code==201:
            return redirect('/login')
        else:
            return redirect('/register')
    else:
        return render_template("register.html")


@app.route("/profile")
def profile():
    if 'username' in session:
        # email = session['email']
        # name = session['name']
        username = session['username']
        followed_list = requests.get(f'{api}/follow/{username}')
        profile_posts = requests.get(f'{api}/profile/{username}')
        userprofile = requests.get(f'{api}/user/{username}')
        follower_list = requests.get(f'{api}/follow/{username}')


        if followed_list.status_code == 200 and profile_posts.status_code == 200:
            followed = followed_list.json()

            allposts = profile_posts.json()

            userp = userprofile.json()

            follower = follower_list.json()
            # print(follower)


            followed = followed[0]
            follower = follower[1]



            return render_template('profile.html', username = username, followed = followed, allposts = allposts, userp = userp, follower = follower)
        else:
            return 'OOPS!!'
    else:
        return redirect('/login')

@app.route("/editprofile",methods=["GET","POST"] )
def editprofile():
    error = None
    if 'username' in session:
        username = session['username']

        if request.method == 'GET':
            x = requests.get(f'{api}/user/{username}')

            if x.status_code == 200:
                esp = x.json()
                # user_password = resp['password']
                # session['username'] = resp['username']
                # return redirect('/profile')
                return render_template('editprofile.html', user = esp)

        if request.method == 'POST':
            data = request.form
            name = request.form['name']
            new_username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                err_msg = "Your password didn't match"
                return redirect('/editprofile', err_msg=err_msg)

            data = {}
            if name:
                data['name'] = name
            if new_username:
                data['username'] = new_username
            # if email:
            #     data['email'] = email
            
            updated_user = requests.put(f'{api}/user/{username}', json=data)
            # print(updated_user)

            if updated_user.status_code == 201:
                if new_username:
                    x = requests.get(f'{api}/user/{new_username}')

                    if x.status_code == 200:
                        resp = x.json()
                        user_password = resp['password']
                        session['username'] = resp['username']
                        return redirect('/profile')

                    else:
                        return "NO DATA"

                else:
                    x = requests.get(f'{api}/user/{username}')

                    if x.status_code == 200:
                        resp = x.json()
                        user_password = resp['password']
                        session['username'] = resp['username']
                        return redirect('/profile')

                    else:
                        return "NO DATA"

            else:
                error = updated_user.text
                return redirect(url_for('editprofile'))
    else:    
        return render_template('/login')

@app.route('/delete')
def delete_profile():
    if "username" in session:
        username = session['username']
        del_user = requests.delete(f'{api}/user/{username}')
        if del_user.status_code == 200:
            resp = make_response(redirect(url_for('index')))
            resp.set_cookie('user', expires=0)
            return redirect('/')
    return redirect('/login')




@app.route("/addpost", methods=['GET', 'POST'])
def addpost():
    if 'username' in session:
        if request.method == 'POST':
            img = request.files['img']
            username = session['username']
            title = request.form['title']
            body = request.form['body']

            n_post = requests.post(f'{api}/posts', files={ 'img':(img.filename, img.stream, img.mimetype), 'username': (None, username), 'title': (None, title), 'body': (None, body) })
            # new = n_post.json()
            if n_post.status_code == 201:
                return redirect('/feed')
            
            else:
                return redirect('/addpost')

        if request.method == 'GET':
            return render_template('/addpost.html')
    else:
        return render_template('/login')


@app.route("/updatepost/<int:post_id>", methods=['GET', 'POST'])
def updatepost(post_id):
    if 'username' in session:
        if request.method == 'POST':
            data = request.form
            update_post = requests.put(f'{api}/posts/{post_id}', json=data)
            # new = update_post.json()
            if update_post.status_code == 201:
                return redirect('/feed')
            else:
                return redirect(url_for('updatepost', post_id=post_id))

        if request.method == 'GET':
            old_post = requests.get(f'{api}/posts/{post_id}')
            if old_post.status_code == 200:
                post = old_post.json()
                # return redirect('/feed')
                return render_template('updatepost.html', post=post)

    else:
        return redirect('/login')


@app.route("/deletepost/<int:post_id>")
def deletepost(post_id):
    if 'username' in session:
        x = requests.delete(f'{api}/posts/{post_id}')
        if x.status_code == 204:
            return redirect('/mypost')
        else:
            return "error"

    else:
        return redirect('/login')


@app.route("/mynetwork",methods=["GET","POST"])
def mynetwork():
    if "username" in session:
        username = session['username']
        
        network = requests.get(f'{api}/allusers')

        if network.status_code == 200:
            netlist = network.json()

            return render_template('mynetwork.html', network=netlist, username=username)

        else:
            return "OOPS!!"
    else:
        return redirect('/login')

@app.route('/follow/<string:followed>')
def ofollow(followed):
    if 'username' in session:
        follower = session['username']

        x = requests.post(f'{api}/follow', json={'follower':follower, 'followed':followed})
        if x.status_code == 201:
            return redirect(url_for('new', username=followed))
        else:
            return redirect(url_for('mynetwork'))
    else:
        return redirect('/login')

@app.route('/unfollow/<string:followed>')
def ounfollow(followed):
    if 'username' in session:
        follower = session['username']
        x = requests.delete(f'{api}/follow', json={'follower':follower, 'followed':followed})
        # print(x.json())
        if x.status_code == 200:
            return redirect(url_for('new', username=followed))
        else:
            return redirect(url_for('mynetwork'))
    else:
        return redirect('/login')


@app.route('/like/<string:followed>')
def like(followed):
    if 'username' in session:
        follower = session['username']

        x = requests.post(f'{api}/follow', json={'follower':follower, 'followed':followed})
        if x.status_code == 201:
            return redirect(url_for('new', username=followed))
        else:
            return redirect(url_for('mynetwork'))
    else:
        return redirect('/login')


@app.route('/new/<string:username>')
def new(username):
    if 'username' in session:
        myusername = session['username']
        new_username = username
        new = requests.get(f'{api}/user/{new_username}')
        followedlist = requests.get(f'{api}/follow/{myusername}')
        followerlist = requests.get(f'{api}/follow/{new_username}')
        new_posts = requests.get(f'{api}/userpost/{new_username}')

        if followedlist.status_code == 200 and followerlist.status_code == 200 and new_posts.status_code == 200 and new.status_code == 200:
            new_details = new.json()
            known = followedlist.json()
            # print(known)
            unknown = followerlist.json()
            newp = new_posts.json()
            
            followed = unknown[0]
            follower = unknown[1]

            n_email = new_details['email']
            n_name = new_details['name']
            n_username = new_details['username']

            known = known[1]
            # print(len(known), followed)
            flag = 0
            if len(known) < 1:
                flag = 1
            else:
                for w in known:
                    # print(w['followed'],new_username)
                    if w['followed'] == new_username:
                        flag = 0
                    if w['followed'] != new_username:
                        flag = 1
            return render_template('new.html', myusername=myusername,  new_posts= new_posts, follower=follower, followed=followed, 
                                            new_username=new_username, flag=flag, new_details=new_details, 
                                            newp=newp, n_email=n_email, n_name=n_name, n_username=n_username)
        else:
            return "OOHHOO!!"
    else:
        return redirect('/login')
        
@app.route('/search', methods=['POST'])
def search():
    if 'username' in session:
        if request.method == 'POST':
            find = request.form['find']
            # print(find)
            x = requests.get(f'{api}/search',json={"find":find})

            if x.status_code == 200:
                ans = x.json()
                return render_template('search.html', ans=ans)

            return "error"
    else:
        return redirect('/login')

@app.route("/logout")
def userLogout():
    resp = make_response(redirect(url_for('index')))
    resp.set_cookie('user', expires=0)
    return resp



if __name__ == "__main__":
  app.run(
      debug=True,
      port=5050
  )