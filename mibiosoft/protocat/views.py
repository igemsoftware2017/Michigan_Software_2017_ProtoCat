from django.shortcuts import *
from django.http import *
from .models import *
from django.contrib.auth import *
from django.db.models import Q
from django.db import connection

# Create your views here.
def index(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	context = {
		'title': 'ProtoCat',
		'current_profile_info': current_profile_info,
	}
	print ("RENDERING INDEX")
	print(len(connection.queries))
	return render(request, 'index.html', context)

def category_default(request):
	current_parent = None
	return category_browser(request, current_parent)

def category_specific(request, category_id):
	current_parent = Category.objects.get(id = category_id)
	return category_browser(request, current_parent)

def category_browser(request, current_parent):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	categories = Category.objects.filter(parent_category = current_parent)
	protocols = Protocol.objects.filter(category = current_parent)

	text = 'ProtoCat'
	context = {
		'title': 'ProtoCat - Browse Categories',
		'parent_category': current_parent,
		'categories': categories,
		'protocols': protocols,
		'current_profile_info': current_profile_info,
	}
	print(len(connection.queries))
	return render(request, 'category_browser.html', context)

def protocol(request, protocol_id):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	protocol = Protocol.objects.get(id = protocol_id)
	protocol_steps = ProtocolStep.objects.filter(protocol = protocol).order_by('step_number')
	protocol_reagents = ReagentForProtocol.objects.filter(protocol = protocol)
	next_protocols = Protocol.objects.filter(previous_revision = protocol)
	for next_protocol in next_protocols:
		print(next_protocol)
	step_notes = ProtocolStepNote.objects.filter(protocol = protocol)
	try:
		text_reagents = TextReagent.objects.get(protocol = protocol)
	except TextReagent.DoesNotExist:
		text_reagents = None

	aggregated_reagents = None
	if (protocol_reagents != None):
		aggregated_reagents = list(protocol_reagents[:1])
		for protocol_reagent in protocol_reagents:
			to_add = True
			for aggregated_reagent in aggregated_reagents:
				if (protocol_reagent.reagent_type == 1 and aggregated_reagent.reagent == protocol_reagent.reagent and aggregated_reagent.unit == protocol_reagent.unit):
					to_add = False

			if (to_add):
				aggregated_reagents.append(protocol_reagent)

	context = {
		'title': protocol.title,
		'protocol': protocol,
		'protocol_steps': protocol_steps,
		'protocol_reagents': protocol_reagents,
		'next_protocols': next_protocols,
		'step_notes': step_notes,
		'text_reagents': text_reagents,
		'aggregated_reagents': aggregated_reagents,
		'current_profile_info': current_profile_info,
	}
	print (len(connection.queries))

	print ("RENDERING PROTOCOL")

	return render(request, 'protocol.html', context)

def user(request, user_id):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	user = ProfileInfo.objects.get(id = user_id)
	user_created_protocols = Protocol.objects.filter(author = user).order_by('-upload_date')
	user_created_notes = ProtocolStepNote.objects.filter(author = user).order_by('-upload_date')
	user_rated_protocols = ProtocolRating.objects.filter(person = user).order_by('-score')

	data = list(user_created_protocols) + list(user_created_notes)
	sorted_data = sorted(data, key=lambda obj: obj.upload_date, reverse=True)

	title = 'ProtoCat - ' + str(user.user)

	context = {
		'title': title,
		'current_profile_info': current_profile_info,
		'profile_info': user,
		'user_created_protocols': user_created_protocols,
		'user_rated_protocols': user_rated_protocols,
		'notes': user_created_notes
	}
	print(len(connection.queries))

	return render(request, 'user.html', context)

def sign_up(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	context = {
		'title': 'ProtoCat - Sign Up',
		'current_profile_info': current_profile_info,
	}
	return render(request, 'sign_up.html', context)

def submit_sign_up(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	username = request.POST['username']
	password = request.POST['password']
	user = User.objects.create_user(username, 'lennon@thebeatles.com', password)
	profile_info = ProfileInfo(user = user)
	profile_info.save()
	print(profile_info.id)
	print(len(connection.queries))
	return HttpResponseRedirect('/')

def login_user(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	context = {
		'title': 'ProtoCat - Login',
		'current_profile_info': current_profile_info,
	}
	return render(request, 'login.html', context)

def submit_login(request):
	username = request.POST['username']
	password = request.POST['password']
	user = authenticate(username = username, password = password)

	if user is not None:
		# the pasword verified for the user
		if user.is_active:
			login(request, user)
			profile_info = ProfileInfo.objects.get(user = user)
			return HttpResponseRedirect('/user/' + str(profile_info.id) + '/')
		else:
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/login/')

def logoff(request):
	logout(request)
	return HttpResponseRedirect('/')

def reagent(request, reagent_id):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	act_reagent = Reagent.objects.get(id = reagent_id)
	title = 'ProtoCat - ' + str(act_reagent)
	context = {
		'title': title,
		'current_profile_info': current_profile_info,
	}
	return render(request, 'reagent.html', context)

def about(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None
	context = {
		'title': 'ProtoCat',
		'current_profile_info': current_profile_info,
	}
	print ("RENDERING ABOUT")
	return render(request, 'about.html', context)

def search(request):
	text_filter = request.POST['text_filter']
	try:
		order = request.POST['order']
	except:
		order = 'title'
	current_profile_info = request.user

	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None

	results = Protocol.objects.filter(Q(title__icontains = text_filter) | Q(description__icontains = text_filter)).order_by(order)
	context = {
		'title': 'ProtoCat',
		'results': results,
		'current_profile_info': current_profile_info,
	}
	print(len(connection.queries))
	print ("RENDERING SEARCH")
	return render(request, 'search.html', context)

def submit_rating(request):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):

		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		new_value = request.POST['NewValue']
		protocol_id = request.POST['id']
		protocol = Protocol.objects.get(id = protocol_id)

		try:
			old_rating = ProtocolRating.objects.get(person = current_profile_info, protocol = protocol)
			old_rating.score = new_value
			old_rating.save()
		except:
			rating = ProtocolRating(person = current_profile_info, score = new_value, protocol = protocol)
			rating.save()
	context = {
		'title': 'ProtoCat',
		'current_profile_info': current_profile_info,
	}
	return render(request, 'index.html', context)


def upload_default(request):
	current_data = None
	return upload_page(request, current_data)

def upload_branch(request, protocol_id):
	#current_parent = Category.objects.get(id = category_id)
	current_data = None
	return upload_page(request, current_data)

def upload_page(request, current_data):
	current_profile_info = request.user
	if (not current_profile_info.is_anonymous()):
		current_profile_info = ProfileInfo.objects.get(user = current_profile_info)
		print(current_profile_info)
	else:
		current_profile_info = None

	context = {
		'title': 'ProtoCat - Browse Categories',
		'current_profile_info': current_profile_info,
	}
	print(len(connection.queries))
	return render(request, 'upload_protocol.html', context)
