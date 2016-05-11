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
	next_protocols = Protocol.objects.filter(last_revision = protocol)
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
		'title': 'ProtoCat',
		'protocol': protocol,
		'protocol_steps': protocol_steps,
		'protocol_reagents': protocol_reagents,
		'next_protocols': next_protocols,
		'step_notes': step_notes,
		'text_reagents': text_reagents,
		'aggregated_reagents': aggregated_reagents,
	}

	print ("RENDERING PROTOCOL")
	print(protocol)
	for e in protocol_steps:
		print(e)
	for e in protocol_reagents:
		print(e)
	print()
	print()
	for e in aggregated_reagents:
		print(e)

	return render(request, 'protocol.html', context)
