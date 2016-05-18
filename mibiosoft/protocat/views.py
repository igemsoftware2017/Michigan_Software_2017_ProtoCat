from django.shortcuts import *
from django.http import *
from .models import *
from django.contrib.auth import *

# Create your views here.
def index(request):
	context = {
		'title': 'ProtoCat'
	}
	print ("RENDERING INDEX")
	return render(request, 'index.html', context)

def category_default(request):
	current_parent = None
	return category_browser(request, current_parent)

def category_specific(request, category_id):
	current_parent = Category.objects.get(id = category_id)
	return category_browser(request, current_parent)

def category_browser(request, current_parent):
	categories = Category.objects.filter(parent_category = current_parent)
	protocols = Protocol.objects.filter(category = current_parent)

	text = 'Protocat'
	context = {
		'title': 'Protocat - Browse Categories',
		'parent_category': current_parent,
		'categories': categories,
		'protocols': protocols,
	}

	return render(request, 'category_browser.html', context)

def protocol(request, protocol_id):
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
	}

	print ("RENDERING PROTOCOL")

	return render(request, 'protocol.html', context)

def user(request, user_id):
	user = ProfileInfo.objects.get(id = user_id)
	user_created_protocols = Protocol.objects.filter(author = user).order_by('-upload_date')
	user_created_notes = ProtocolStepNote.objects.filter(author = user).order_by('-upload_date')
	user_rated_protocols = ProtocolRating.objects.filter(person = user).order_by('-score')

	data = list(user_created_protocols) + list(user_created_notes)
	sorted_data = sorted(data, key=lambda obj: obj.upload_date, reverse=True)

	title = 'Protocat - ' + str(user.user)

	context = {
		'title': title,
		'profile_info': user,
		'user_created_protocols': user_created_protocols,
		'user_rated_protocols': user_rated_protocols,
		'notes': user_created_notes
	}

	return render(request, 'user.html', context)

def sign_up(request):
	context = {
		'title': 'Protocat - Sign Up',
	}
	return render(request, 'sign_up.html', context)

def submit_sign_up(request):
	username = request.POST['username']
	password = request.POST['password']
	user = User.objects.create_user(username, 'lennon@thebeatles.com', password)
	profile_info = ProfileInfo(user=user)
	profile_info.save()
	print(profile_info.id)
	return HttpResponseRedirect('/')

def login_user(request):
	context = {
		'title': 'Protocat - Login',
	}
	return render(request, 'login.html', title)

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
	act_reagent = Reagent.objects.get(id = reagent_id)
	title = 'Protocat - ' + str(act_reagent)
	context = {
		'title': title,
	}
	return render(request, 'reagent.html', context)
