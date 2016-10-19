from django.test import TestCase, Client
from django.contrib.auth import *
from datetime import datetime
from .models import *

class ProtocolTestCase(TestCase):
	def test_invalid_upload(self):
		try:
			user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
			user.save()
			profile_info = ProfileInfo(user = user)
			profile_info.save()
		except:
			pass
		c = Client()

		# test security for API

		logged_in = c.login(username='test12345', password='IncorrectPassword')
		response = c.post('/api/protocol/',
			{
				"title":"Mini-Prep Protocol",
				"description":"<p>This protocol is for purifying DNA&nbsp;obtained from a small culture.</p>","materials":"",
				"change_log":"",
				"protocol_steps":[
					{
						"title":"",
						"step_number":1,
						"time":60,
						"action":"<p>Transfer bacterial cells to a micro centrifuge tube. Centrifuge for 1 minute at high speed. Discard supernatant.</p>","warning":"","time_scaling":2,"reagents":[]},{"title":"","step_number":2,"time":None,"action":"<p>Resuspend bacterial cells in 250ul buffer P1(kept at ~4&deg;C).</p>",
						"warning":"",
						"time_scaling":2
					},
					{
						"title":"",
						"step_number":3,
						"time":None,
						"action":"<p>Add 250uls Buffer P2 and mix by inverting 4-6 times.</p>",
						"warning":"",
						"time_scaling":2
					},
					{"title":"","step_number":4,"time":None,"action":"<p>Add 350uls Buffer N3 and mix immediately by inverting 4-6 times.</p>","warning":"","time_scaling":2,"reagents":[]
					},
					{"title":"","step_number":5,"time":600,"action":"<p>Centrifuge for 10 minutes.</p>","warning":"","time_scaling":2,"reagents":[]},{"title":"","step_number":6,"time":None,"action":"<p>Transfer supernatant to spin column by decanting.</p>","warning":"","time_scaling":2,"reagents":[]},{"title":"","step_number":7,"time":60,"action":"<p>Wash the spin column by adding 500uls of buffer PB and centrifuge for 1 minute. Discard flow-through.</p>","warning":"","time_scaling":2,"reagents":[]},
					{"title":"","step_number":8,"time":None,"action":"<p>Wash spin column by adding 750uls of buffer PE and centrifuge for 1 minute. Discard flow-though and centrifuge for an additional minute to remove residual wash buffer.</p>","warning":"","time_scaling":2,"reagents":[]},
					{"title":"","step_number":9,"time":None,"action":"<p>To elute DNA, place spin column in a clean 1.5ml micro centrifuge tube.</p>\n<div>&nbsp;</div>","warning":"","time_scaling":2,"reagents":[]},
					{"title":"","step_number":10,"time":None,"action":"<div>Add 25uls of ultra pure water, let stand for 1 minute and centrifuge for 1 minute.</div>","warning":"","time_scaling":2,"reagents":[]},
					{"title":"","step_number":11,"time":None,"action":"<p>Repeat step 10 to have a total of 50uls DNA, eluting with 25uls twice instead of doing 50uls once will give higher concentrated DNA.</p>","warning":"","time_scaling":2,"reagents":[]}
				]
			})
		assert(response.status_code == 403)
		assert(response.content == '{"detail":"Authentication credentials were not provided."}')

		print("PASSED ANON USER PROTOCOL UPLOAD TEST")

	def test_valid_upload(self):
		try:
			user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
			user.save()
			profile_info = ProfileInfo(user = user)
			profile_info.save()
		except:
			pass
		c = Client()
		user = authenticate(username = "test12345", password = "NotPassword")
		user = ProfileInfo.objects.get(user = user)

		# test creation of empty protocol
		try:
			p = Protocol.objects.get(id = 2000)
			p.delete()
		except:
			pass

		protocol = Protocol.objects.create(
			title = "Title",
			description = "description",
			change_log = "Nothing new",
			author = user,
			id = 2000
		)
		protocol.save()

		response = c.get('/api/protocol/' + str(protocol.id) + '/')
		assert(response.content.split('upload_date')[0] == 
			'{"url":"http://testserver/api/protocol/2000/","protocol_steps":[],"title":"Title","category":null,"')

		print("PASSED LOGGED IN USER PROTOCOL UPLOAD TEST")

class CategoryTestCase(TestCase):
	def test_invalid_upload(self):
		try:
			user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
			user.save()
			profile_info = ProfileInfo(user = user)
			profile_info.save()
		except:
			pass
		c = Client()

		# test security for API

		logged_in = c.login(username='test12345', password='IncorrectPassword')
		response = c.post('/api/category/',
			{
				"title": "Purification",
				"description": "Protocols used to isolate a desired product",
				"parent_category": None
			})
		assert(response.status_code == 403)
		assert(response.content == '{"detail":"Authentication credentials were not provided."}')

		print("PASSED ANON USER CATEGORY UPLOAD TEST")

	def test_valid_upload(self):
		try:
			user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
			user.save()
			profile_info = ProfileInfo(user = user)
			profile_info.save()
		except:
			pass
		c = Client()
		# test API working
		logged_in = c.login(username='test12345', password='NotPassword')
		response = c.post('/api/category/',
			{
				"title": "Purification",
				"description": "Protocols used to isolate a desired product",
				"parent_category": None
			})
		assert(response.status_code == 200)
		assert(response.content == '{"status":"Saved category"}')

		print("PASSED LOGGED IN USER CATEGORY UPLOAD TEST")

class UserTestCase(TestCase):
	def test_creation_and_login(self):
		user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
		user.save()
		profile_info = ProfileInfo(user = user)
		profile_info.save()
		print("PASSED USER CREATION TEST")

class ReagentTestCase(TestCase):
	def test_invalid_creation(self):
		user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
		user.save()
		profile_info = ProfileInfo(user = user)
		profile_info.save()
		c = Client()
		# test API working
		logged_in = c.login(username='test12345', password='BadPassword')
		response = c.post('/api/reagent/', {
			"name": "agarose",
			"website": "agarose.com",
			"description": "does something"
		})
		assert(response.status_code == 403)
		assert(response.content == '{"detail":"Authentication credentials were not provided."}')

		print("PASSED ANON USER REAGENT UPLOAD TEST")		

	def test_valid_creation(self):
		user = User.objects.create_user("test12345", "hi@gmail.com", "NotPassword")
		user.save()
		profile_info = ProfileInfo(user = user)
		profile_info.save()
		c = Client()
		# test API working
		logged_in = c.login(username='test12345', password='NotPassword')
		response = c.post('/api/reagent/', {
			"name": "agarose",
			"website": "agarose.com",
			"description": "Does a thing"
		})
		assert(response.status_code == 200)
		print("PASSED LOGGED IN USER REAGENT UPLOAD TEST")

class ViewingTests(TestCase):
	def test_generic_pages_logged_in(self):
		c = Client()
		''' creating a user'''
		user = User.objects.create_user(username="test12345", password="NotPassword")
		user.save()
		profile_info = ProfileInfo(user = user)
		profile_info.save()
		c.login(username='test12345', password="NotPassword")

		response = c.get('/about/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/login/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/browse/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/upload/')
		self.assertEqual(response.status_code, 200)
		response = c.post('/search/', {
			'text_filter': ""
		})
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/category/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/protocol/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/reagent/')
		self.assertEqual(response.status_code, 200)

		print("PASSED LOGGED IN USER TEST")

	def test_generic_pages_logged_in(self):
		c = Client()

		response = c.get('/about/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/login/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/browse/')
		self.assertEqual(response.status_code, 200)
		#only banned page
		response = c.get('/upload/')
		self.assertEqual(response.status_code, 302)
		response = c.post('/search/', {
			'text_filter': ""
		})
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/category/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/protocol/')
		self.assertEqual(response.status_code, 200)
		response = c.get('/api/reagent/')
		self.assertEqual(response.status_code, 200)
		print("PASSED ANON USER TEST")