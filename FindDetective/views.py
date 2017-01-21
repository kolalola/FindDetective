from models import Users,Posts,UsersRoles,Requests,Roles
from pyramid_sqlalchemy import Session as DBSession
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )
from forms import BlogCreateForm,RegistrationForm,ProposeForm
from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember, forget


def BlogIndex(request):
    posts = DBSession.query(Posts).all()
    username = request.authenticated_userid
    if username:
        user = DBSession.query(Users).filter_by(login=username).first()
        role=DBSession.query(Roles).filter_by(nameRole="Detective").first()
        userrole=DBSession.query(UsersRoles).filter_by(idUser=user.idUser,IdRole=role.idRole).first()
        if userrole:
            return {'posts': reversed(posts),'propose':True}
        else:
            return {'posts': reversed(posts)}
    else:
        return {'posts': reversed(posts)}

def ReadPost(request):
    username = request.authenticated_userid
    postid = request.matchdict['idPost']
    post = DBSession.query(Posts).filter_by(idPost=postid).first()
    proposes=[]
    if (post is None):
        return HTTPNotFound('No such page')
    title = post.title
    text = post.text
    proposes = DBSession.query(Requests).filter_by(idPost=postid)
    if post.idUser==-1:
        return {'title':title,'text':text,'proposes':proposes}
    else:
        if username:
            user = DBSession.query(Users).filter_by(login=username).first()
            userpost = DBSession.query(Posts).filter_by(idPost=postid, idUser=user.idUser).first()
            if userpost:
                return {'title': title, 'text': text,'proposes':proposes,'post': post}
        return {'title': title, 'text': text}

def AddPost(request):
    entry = Posts()
    form = BlogCreateForm(request.POST)
    if request.method == 'POST' and form.validate():
        form.populate_obj(entry)
        username = request.authenticated_userid
        if username:
            user=DBSession.query(Users).filter_by(login=username).first()
            entry.idUser=user.idUser
        else:
            entry.idUser=-1;
        DBSession.add(entry)
        return HTTPFound(location=request.route_url('index'))
    return {'form': form}

def Sign_in_out(request):
    username = request.POST.get('username')
    if username:
        user = DBSession.query(Users).filter_by(login=username).first()
        if user and user.verify_password(request.POST.get('password')):
            headers = remember(request, user.login)
        else:
            headers = forget(request)
    else:
        headers = forget(request)
    return HTTPFound(location=request.route_url('index'), headers=headers)

def Register(request):
    entry=Users()
    form = RegistrationForm(request.POST)
    if request.method == 'POST' and form.validate():
        entry.login=form.username.data
        entry.mail=form.mail.data
        entry.set_password(form.password.data)
        for dic in form.role.choices:
            if dic[0]==form.role.data:
                role=dic[1]
        user = DBSession.query(Users).filter_by(login=entry.login).first()
        if user:
            return dict(exist='Такой пользователь уже существует')
        Role=DBSession.query(Roles).filter_by(nameRole=role).first()
        DBSession.add(entry)
        user = DBSession.query(Users).filter_by(login=entry.login).first()
        DBSession.add(UsersRoles(idUser=user.idUser,IdRole=Role.idRole))
        return HTTPFound(location=request.route_url('index'))
    return {'form':form}

def Propose(request):
    username = request.authenticated_userid
    if username:
        user_detective = DBSession.query(Users).filter_by(login=username).first()
        userRole = DBSession.query(UsersRoles).filter_by(idUser=user_detective.idUser).first()
        idRole = DBSession.query(Roles).filter_by(nameRole="Detective").first().idRole
        if userRole.IdRole==idRole:
            idPost = request.matchdict['idPost']
            entry = Requests()
            form = ProposeForm(request.POST)

            if request.method == 'POST' and form.validate():
                entry.description = form.description.data
                entry.phone = form.phone.data
                user = DBSession.query(Users).filter_by(login=username).first()
                entry.idUser = user.idUser
                entry.idPost = idPost
                entry.title=form.title.data
                DBSession.add(entry)
                return HTTPFound(location=request.route_url('read',idPost=idPost))
            return {'form': form, 'idPost': idPost}
        else:
            return HTTPFound(location=request.route_url('index'))
    else:
            return HTTPFound(location=request.route_url('register'))

def DeletePost(request):
    username=request.authenticated_userid
    user=DBSession.query(Users).filter_by(login=username).first()
    idPost=request.matchdict['idPost']
    post=DBSession.query(Posts).filter_by(idPost=idPost).first()

    if user.idUser==post.idUser:
        posts = DBSession.query(Posts).filter_by(idPost=idPost).first()
        DBSession.delete(posts)
        rqsts=DBSession.query(Requests).filter_by(idPost=idPost)
        for rqst in rqsts:
            DBSession.delete(rqst)
        return HTTPFound(location=request.route_url('index'))

def ReadPropose(request):
    idRequest=request.matchdict['idRequest']
    propose=DBSession.query(Requests).filter_by(idRequest=idRequest).first()
    user=DBSession.query(Users).filter_by(idUser=propose.idUser).first()
    return {'propose':propose,'user':user}
