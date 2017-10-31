from rest_framework import permissions
from rest_framework import renderers
from rest_framework import viewsets
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import permissions
from .permissions import *
from .models import *
from .serializers import *
import bleach

ACCEPTABLE_TAGS = [
	'a',
	'abbr',
	'acronym',
	'address',
	'area',
	'b',
	'bdo',
	'big',
	'blockquote',
	'br',
	'button',
	'caption',
	'center',
	'cite',
	'code',
	'col',
	'colgroup',
	'dd',
	'del',
	'dfn',
	'dir',
	'div',
	'dl',
	'dt',
	'em',
	'fieldset',
	'font',
	'form',
	'h1',
	'h2',
	'h3',
	'h4',
	'h5',
	'h6',
	'hr',
	'i',
	'img',
	'input',
	'ins',
	'kbd',
	'label',
	'legend',
	'li',
	'map',
	'menu',
	'ol',
	'optgroup',
	'option',
	'p',
	'pre',
	'q',
	's',
	'samp',
	'select',
	'small',
	'span',
	'strike',
	'strong',
	'sub',
	'sup',
	'table',
	'tbody',
	'td',
	'textarea',
	'tfoot',
	'th',
	'thead',
	'u',
	'tr',
	'tt',
	'u',
	'ul',
	'var',
]

ACCEPTABLE_ATTRIBUTES = {
	'*': ['style', 'width', 'height', 'class'],
	'img': ['src', 'alt'],
	'a': ['href'],
	'span': ['data-reagent-number', 'contenteditable']
}

ACCEPTABLE_STYLES = [
	'color',
	'font-weight',
	'text-align',
	'font-size',
	'font-family',
	'font-weight',
	'float',
	'line-height'
]


class ProtocolViewSet(viewsets.ModelViewSet):
	"""
	This endpoint presents the stored protocols.

	Here you can only POST new protocols if you are logged in. Otherwise,
	you can GET the information for all protocols by doing a GET request
	to /api/protocol/ or for a specific protocol by doing a GET request to
	/api/protocol/{id}. The GET requests return the main information posted by
	the original poster as well as the individual ratings and comments to show
	alongside the protocol.

	When you POST a new protocol, you only need to submit the title, description,
	change log, materials, protocol steps, and the id of the previous revision
	(null if it is not a revision) in the JSON format to /api/protocol/. The way
	to format the protocol steps is to have the protocol_steps be an array of
	steps, each with their own step number, time (in seconds) to complete the step,
	(-1 if untimed), the action, any warnings, and if the time scales (1 means no
	scaling, 2 means linear scaling).

	To authenticate the user, you must first submit a POST to /api/token/ with
	the username and password. This will send you a token in the header which
	you can send with every request that needs authentication.
	"""
	permission_classes = (IsAuthenticatedOrReadOnlyPUTDisallowed,)
	queryset = Protocol.objects.all()
	serializer_class = ProtocolSerializer

	def create(self, request):
		try:
			protocol = Protocol()
			protocol.title = request.data['title']
			try:
				protocol.category = Category.objects.get(id = request.data['category'])
			except:
				protocol.category = None
			protocol.description = bleach.clean(request.data['description'],
												tags = ACCEPTABLE_TAGS,
												attributes = ACCEPTABLE_ATTRIBUTES,
												styles = ACCEPTABLE_STYLES)
			protocol.change_log = bleach.clean(request.data['change_log'],
												tags = ACCEPTABLE_TAGS,
												attributes = ACCEPTABLE_ATTRIBUTES,
												styles = ACCEPTABLE_STYLES)
			try:
				if (request.data['previous_revision'] != None and request.data['previous_revision'] != "-1"):
					previous_protocol = Protocol.objects.get(id = request.data['previous_revision'])
					protocol.previous_revision = previous_protocol
					protocol.first_revision = previous_protocol.first_revision
			except:
				protocol.previous_revision = None
			protocol.author = request.user.profileinfo
			try:
				protocol.materials = request.data['materials']
			except:
				pass
			step_list = []
			reagent_list = []
			#print('Main protocol finished')
			# go over each step
			i = 0
			#print(request.data)
			for step in request.data['protocol_steps']:
				#print(request.data['protocol_steps'])
				i = i + 1
				# fill out step info
				protocol_step = ProtocolStep()
				if (step['title'] != "" and step['title'] != None):
					protocol_step.title = step['title']
				protocol_step.step_number = step['step_number']
				if (step['time'] != None):
					protocol_step.time = int(step['time'])
				protocol_step.action = bleach.clean(step['action'],
													tags = ACCEPTABLE_TAGS,
													attributes = ACCEPTABLE_ATTRIBUTES,
													styles = ACCEPTABLE_STYLES)
				if (step['warning'] != ""):
					protocol_step.warning = bleach.clean(step['warning'],
														tags = ACCEPTABLE_TAGS,
														attributes = ACCEPTABLE_ATTRIBUTES,
														styles = ACCEPTABLE_STYLES)

				protocol_step.time_scaling = int(step['time_scaling'])
				if 'reagents' in step:
					# make each reagent
					for reagent in step['reagents']:
						# fill all data parts
						step_reagent = ReagentForProtocol()
						step_reagent.scaling_type = reagent['scaling_type']
						step_reagent.reagent_type = reagent['reagent_type']
						step_reagent.amount = float(reagent['amount'])
						step_reagent.unit = reagent['unit']
						step_reagent.number_in_step = int(reagent['number_in_step'])
						step_reagent.significant_figures = int(reagent['significant_figures'])
						if (reagent['preserve_units'] != None and reagent['preserve_units'] != -1):
							step_reagent.preserve_units = reagent['preserve_units']
						step_reagent.protocol_step_number = step['step_number']
						linked_reagent = ""
						# get reagent to link to this one
						try:
							linked_reagent = Reagent.objects.get(id = reagent['reagent_id'])
						except:
							linked_reagent = Reagent.objects.get(id = reagent['reagent_id']['id'])
						if (reagent['display_name'] != None and reagent['display_name'] != -1):
							step_reagent.display_name = reagent['display_name']
						else:
							step_reagent.display_name = linked_reagent.name
						step_reagent.reagent = linked_reagent
						reagent_list.append(step_reagent)
				step_list.append(protocol_step)
				#print("Step " + i + " completed")
			protocol.num_steps = i
			#print(i)
			protocol.save()
			if protocol.first_revision == None:
				protocol.first_revision = protocol
				protocol.save()

			# save each step and each reagent
			for step in step_list:
				step.protocol = protocol
				step.save()
				for reagent in reagent_list:
					reagent.protocol = protocol
					# if the reagent is supposed to be associated with that step
					# associate them
					if (reagent.protocol_step_number == step.step_number):
						reagent.protocol_step = step
						reagent.save()

			for question in request.data["protocol_questions"]:
				print(question)
				new_question = None
				if question["type"] == "Poll":
					print("METRIC ENUM QUESTION")
					new_question = MetricEnumQuestion()
					new_question.protocol = protocol
					new_question.save()
					for option in question["options"]:
						new_opt = MetricEnumOption()
						new_opt.enum_question = new_question
						new_opt.option_text = option
						new_opt.save()
				else:
					print("METRIC QUESTION")
					new_question = MetricQuestion()
					new_question.protocol = protocol
					new_question.question_type = question["type"]

				new_question.question_text = question["question_text"]
				new_question.save()

			print(protocol.metric_questions)

			return Response({'success': True, 'location': '/protocol/' + str(protocol.id)})
		except Exception as inst:
			print(inst)
			return Response({'success': False, 'error': str(inst)})

class ProfileViewSet(viewsets.ModelViewSet):
	"""
	This endpoint presents our user system.

	Here you can view the public information of any user, such as the username,
	list of protocols they made, and other basic info. You can only PUT
	information to the account you are logged in with, but you can always GET
	others' basic information.

	To authenticate the user, you must first submit a POST to /api/token/ with
	the username and password. This will send you a token in the header which
	you can send with every request that needs authentication.
	"""
	permission_classes = (IsUserOrReadOnly,)
	http_method_names = ['get', 'options', 'head', 'put']
	queryset = ProfileInfo.objects.all()
	serializer_class = ProfileSerializer

class CategoryViewSet(viewsets.ModelViewSet):
	"""
	This endpoint shows our category system.

	Here, you can POST new categories if you are logged in, otherwise you can
	view the current categories and infomation about them. If you are POSTing a
	new category, be sure to link it to a parent category by id or keep the
	value as null if you do not want a parent category.

	To authenticate the user, you must first submit a POST to /api/token/ with
	the username and password. This will send you a token in the header which
	you can send with every request that needs authentication.
	"""
	queryset = Category.objects.all()
	serializer_class = CategorySerializer
	permission_classes = (IsReadOnlyOrAuthenticated,)

	def create(self, request):
		try:
			category = Category()
			category.title = request.data['title']
			category.description = request.data['description']
			try:
				category.parent_category = Category.objects.get(id = request.data['parent_category'])
			except:
				pass
			category.author = request.user.profileinfo
			category.save()
			return Response({'status': 'Saved category'})
		except Exception as inst:
			return Response({'status': 'failed'})

class CategoryBrowser(generics.ListAPIView):
	serializer_class = CategorySerializer
	permission_classes = (IsReadOnly,)
	def get_queryset(self):
		categories = Category.objects.all()
		parent_id = self.request.GET.get('parent_id', None)
		print(parent_id)
		if (parent_id != None):
			categories = categories.filter(parent_category = int(parent_id))
		else:
			categories = categories.filter(parent_category = None)
		return categories

class ReagentViewSet(viewsets.ModelViewSet):
	"""
	This endpoint presents the available reagents in the system.

	Here, you can POST new reagents if you are logged in, otherwise you can
	view our current catalog and infomation about them.

	To authenticate the user, you must first submit a POST to /api/token/ with
	the username and password. This will send you a token in the header which
	you can send with every request that needs authentication.
	"""
	permission_classes = (IsReadOnlyOrAuthenticated,)
	queryset = Reagent.objects.all()
	serializer_class = ReagentSerializer

	def create(self, request):
		try:
			#print(request.data)
			reagent = Reagent()
			reagent.name = request.data['name']
			reagent.website = request.data['website']
			reagent.description = bleach.clean(request.data['description'],
													tags = ACCEPTABLE_TAGS,
													attributes = ACCEPTABLE_ATTRIBUTES,
													styles = ACCEPTABLE_STYLES)
			reagent.save()
			return Response({'success': True, 'location': '/reagent/' + str(reagent.id)})
		except Exception as inst:
			#print(inst)
			return Response({'status': 'failed'})

	def update(self, request, pk=None):
		reagent = Reagent.objects.get(id = pk)
		try:
			reagent.website = request.data['website']
		except:
			pass
		try:
			reagent.description = bleach.clean(request.data['description'],
													tags = ACCEPTABLE_TAGS,
													attributes = ACCEPTABLE_ATTRIBUTES,
													styles = ACCEPTABLE_STYLES)
			console.log(reagent.description)
		except:
			pass
		reagent.save()

		return Response({'success': True, 'location': '/reagent/' + str(reagent.id)})