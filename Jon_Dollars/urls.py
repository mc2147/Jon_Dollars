from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'Jon_Dollars.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    
    #logins here
    url(r'^login/', 'StudentApp.views.FirstPage', name='Login'),
    #url(r'^teacher/$', 'start_map.views.TeacherLogin', name='TeacherLogin'),
	#url(r'^student/$', 'start_map.views.StudentLogin', name='StudentLogin'),
	

    #teacher urls start here
	url(r'^teacher/home$', 'Teacher.views.TeacherHome', name='TeacherHome'),
	url(r'^teacher/good-deeds$', 'Teacher.views.GoodDeeds', name='GoodDeeds'),
	url(r'^teacher/items$', 'Teacher.views.Items', name='Items'),
	url(r'^teacher/settings$', 'Teacher.views.TeacherSettings', name='TeacherSettings'),
	url(r'^teacher/requests$', 'Teacher.views.Requests', name='TeacherRequests'),
	url(r'^teacher/spend-requests$', 'Teacher.views.SpendRequests', name='TeacherSpendRequests'),
	

	#student urls start here
	url(r'^student/home$', 'StudentApp.views.StudentHome', name='StudentHome'),
	url(r'^student/team$', 'StudentApp.views.Team', name='Team'),
	url(r'^student/shop$', 'StudentApp.views.Shop', name='Shop'),
	url(r'^student/inventory$', 'StudentApp.views.Inventory', name='Inventory'),
	url(r'^student/request-point$', 'StudentApp.views.PointRequest', name='PointRequest'),
	url(r'^student/settings$', 'StudentApp.views.StudentSettings', name='StudentSettings'),

	#test urls here
	url(r'^test$', 'testapp.views.Test_1', name='Test_1'),
	url(r'^test_2$', 'testapp.views.Test_Login', name='Test_Login'),
	url(r'^fake_login$', 'testapp.views.Login', name='Login'),
	url(r'^check_login$', 'testapp.views.Check_Login', name='Login'),
	url(r'^login_required$', 'testapp.views.Login_Required', name='Login'),


#	url(r'^test_2$', 'start_map.views.Test_2', name='Test_2'),	
	
#	url(r'^test$', 'start_map.views.Test', name='Test'),	
	
]
