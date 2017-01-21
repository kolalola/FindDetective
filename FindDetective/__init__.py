from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from models import Users,Posts,UsersRoles,Requests,Roles
from pyramid_sqlalchemy import BaseObject as Base,Session
import transaction
import pyramid_sacrud
from pyramid.view import view_config
from views import BlogIndex,ReadPost,AddPost,Sign_in_out,Register,Propose,DeletePost,ReadPropose
import pyramid_jinja2
import pyramid_tm
from pyramid.authentication import AuthTktAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy



if __name__ == '__main__':
    authentication_policy = AuthTktAuthenticationPolicy('somesecret')
    authorization_policy = ACLAuthorizationPolicy()
    settings = {'sqlalchemy.url': 'sqlite:///finDetective.db'}
    config = Configurator(settings=settings,
                          authentication_policy=authentication_policy,
                          authorization_policy=authorization_policy)
    config.include('pyramid_tm')
    config.include('pyramid_sqlalchemy')
    config.include('pyramid_jinja2')



    config.add_route('index', '/')
    config.add_route('read','/posts/{idPost}')
    config.add_route('add','/add')
    config.add_route('auth', '/sign/{action}')
    config.add_route('register','/registration')
    config.add_route('propose','/propose/{idPost}')
    config.add_route('delete','/delete/{idPost}')
    config.add_route('readpropose','/requests/{idRequest}')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view('css','/HTML/jquery-3.1.1.js')


    config.add_view(BlogIndex,route_name='index',renderer='HTML/index.jinja2')
    config.add_view(ReadPost,route_name='read',renderer='HTML/read.jinja2')
    config.add_view(AddPost,route_name='add',renderer='HTML/add.jinja2')
    config.add_view(Sign_in_out,route_name='auth',renderer='string',match_param='action=in')
    config.add_view(Sign_in_out, route_name='auth',renderer='string',match_param='action=out')
    config.add_view(Register,route_name='register',renderer='HTML/register.jinja2')
    config.add_view(Propose,route_name='propose',renderer='HTML/propose.jinja2')
    config.add_view(DeletePost,route_name='delete',renderer='string')
    config.add_view(ReadPropose,route_name='readpropose',renderer='HTML/readpropose.jinja2')

    Base.metadata.create_all()
    print(Session.query(Posts).all())
    #post=Session.query(Posts).filter_by(title='кккк').first()
    #user=Session.query(Users).filter_by(idUser=5).first()
    #Session.delete(user)
    print(Session.query(UsersRoles).all())
    #Requests.__table__.drop()
    print(Session.query(Requests).all())
    print(Session.query(Users).all())
    transaction.commit()
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()