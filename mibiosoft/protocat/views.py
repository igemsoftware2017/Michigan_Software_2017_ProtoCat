from django.shortcuts import *
from django.http import *
from .models import *

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

	print ("RENDERING CATEGORIES")
	for e in categories:
		print(e)
	for e in protocols:
		print(e)

	return render(request, 'category_browser.html', context)

def protocol(request, protocol_id):
	protocol = Protocol.objects.get(id = protocol_id)
	protocol_steps = ProtocolStep.objects.filter(protocol = protocol).order_by('step_number')
	protocol_reagents = ReagentForProtocol.objects.filter(protocol = protocol)

	context = {
		'title': 'ProtoCat',
		'protocol': protocol,
		'protocol_steps': protocol_steps,
	}

	print ("RENDERING PROTOCOL")
	for e in protocol_steps:
		print(e)
	for e in protocol_reagents:
		print(e)

	return render(request, 'index.html', context)
