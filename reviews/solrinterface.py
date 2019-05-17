import requests
# from importlib import reload

"""
This is our only interface with the SOLR service for the amzn-reviews collection
built for the first assignment.
It is simplified as follows
  * We will use only review search and ID (UUID) search
  * And within review search we will filter on score only
"""

##################################

def review_search(kw, sc, start=0):
	return do_query(review_query_dictionary(kw,sc, start))

def id_search(id):
	return do_query(id_query_dictionary(id))

##################################

def test_review_search(): 
	res = review_search("excellent movie", "<= 3")
	return res

def test_id_search():
	res = id_search("c6431db2-635a-416a-a13c-9733391f735c")
	return res

##################################

def do_query(params, port="8983", collection="amazon-reviews"):
	param_arg = "&".join(list(map(lambda p: str(p[0]) + "=" + str(p[1]), list(params.items()))))
	query_string = "http://localhost:" + str(port) + "/solr/" + str(collection) + "/select"
	print("Sending query " + query_string)
	print("Param " + str(params))
	print("args " + str(param_arg))
	r = requests.get(query_string, param_arg)
	if (r.status_code == 200):
		return r.json()['response']
	else:
		raise Exception("Request Error: " + str(r.status_code))


def id_query_dictionary(id):
	return {"q": "id:" + str(id)}

def review_query_dictionary(kw="", sc="", start=0):
	return {"q": "_text_:" + kw + (" AND " + build_score_string(sc) if build_score_string(sc) else ""), "start": start}

def build_score_string(s):
	if (len(s) == 0):
		return None
	else:
		dir, val = s.split()
		if (int(val) < 1 or int(val) > 5):
			raise Exception("Bad score value " + s)
		if dir == "<=":
			return "reviewScore:[0 TO " + str(val) + "]"
		elif dir == ">=":
			return "reviewScore:[" + str(val) + " TO *]"
		else:
			raise Exception("Bad direction value " + s)

test_id_search()