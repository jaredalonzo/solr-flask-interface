import requests
# from importlib import reload

##################################

def review_search(kw, sc, start=0):
	return do_query(review_query_dictionary(kw, sc, start), collection="amazon-reviews")

def id_search(id):
	return do_query(id_query_dictionary(id), collection="amazon-reviews")

def product_asin_search(asin):
	return do_query(asin_query_dictionary(asin), collection="amazon-products")

##################################

def test_review_search(): 
	res = review_search("excellent movie", "<= 3")
	return res

def test_id_search():
	res = id_search("c6431db2-635a-416a-a13c-9733391f735c")
	return res

##################################

def do_query(params, collection, port="8983"):
	param_arg = "&".join(list(map(lambda p: str(p[0]) + "=" + str(p[1]), list(params.items()))))
	query_string = "http://localhost:" + str(port) + "/solr/" + str(collection) + "/select?"
	print("Sending query " + query_string + param_arg)
	print("Param " + str(params))
	print("args " + str(param_arg))
	r = requests.get(query_string, param_arg)
	if (r.status_code == 200):
		return r.json()['response']
	else:
		raise Exception("Request Error: " + str(r.status_code))

def asin_query_dictionary(asin):
	return {"q": "asin:" + str(asin)}

def id_query_dictionary(id):
	return {"q": "id:" + str(id)}

def review_query_dictionary(kw="", sc="", start=0):
	return {"q": "_text_:" + kw + ("%20AND%20" + build_score_string(sc) if build_score_string(sc) else ""), "start": start}

def build_score_string(s):
	if (len(s) == 0):
		return None
	else:
		dir, val = s.split()
		if (int(val) < 1 or int(val) > 5):
			raise Exception("Bad score value " + s)
		if dir == "<=":
			return "overall:[0%20TO%20" + str(val) + "]"
		elif dir == ">=":
			return "overall:[" + str(val) + "%20TO%20*]"
		else:
			raise Exception("Bad direction value " + s)

test_id_search()