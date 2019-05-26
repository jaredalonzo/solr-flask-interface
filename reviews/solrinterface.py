import requests
# from importlib import reload

##################################

def review_search(kw, sc="", start=0):
	return do_query(review_query_dictionary(kw, sc, start), collection="amazon-reviews")

def id_search(id):
	return do_query(id_query_dictionary(id), collection="amazon-reviews")

def product_asin_search(asin):
	return do_query(asin_query_dictionary(asin), collection="amazon-products")

def get_collection_numbers(collection_name):
	return do_query(query_collection(collection_name), collection_name)
##################################

def do_query(params, collection, port="8983"):
	param_arg = "&".join(list(map(lambda p: str(p[0]) + "=" + str(p[1]), list(params.items()))))
	query_string = "http://localhost:" + str(port) + "/solr/" + str(collection) + "/select?"
	r = requests.get(query_string, param_arg)
	if (r.status_code == 200):
		return r.json()
	else:
		raise Exception("Request Error: " + str(r.status_code))

def query_collection(collection_name):
	return {'q': '*:*'}

def asin_query_dictionary(asin):
	return {"q": "asin:" + str(asin)}

def id_query_dictionary(id):
	return {"q": "id:" + str(id)}

def review_query_dictionary(kw="", sc="", start=0):
	return {"spellcheck.q": kw, "spellcheck": "on", "facet.field": "overall", "facet": "on", "facet.sort": "index", "q": "_text_:" + kw + ("%20AND%20" + build_score_string(sc) if build_score_string(sc) else ""), "start": start}

def build_score_string(s):
	if (len(s) == 0):
		return None
	else:
		if (int(s) < 1 or int(s) > 5):
			raise Exception("Bad score value " + s)
		else:
			return "overall:" + str(s)