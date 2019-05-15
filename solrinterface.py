import requests
from importlib import reload

"""
This is our only interface with the SOLR service for the amzn-reviews collection
built for the first assignment.
It is simplified as follows
  * We will use only review search and ID (UUID) search
  * And within review search we will filter on score only
"""

##################################

def review_search(kw, sc, start):
	return do_query(review_query_dictionary(kw,sc, start))

def id_search(id):
	return do_query(id_query_dictionary(id))

##################################

def test_review_search():
	return review_search("excellent movie", "<= 3")

def test_id_search():
	return id_search("4e3fb1e6-1e71-4aa0-9ddd-bc8f8938119c")

##################################

def do_query(params, port="8983", collection="amzn-reviews"):
	param_arg = "&".join(list(map(lambda p: f"{p[0]}={p[1]}", list(params.items()))))
	query_string = f"http://localhost:{port}/solr/{collection}/select"
	print("Sending query " + query_string)
	print("Param " + str(params))
	r = requests.get(query_string, param_arg)
	if (r.status_code == 200):
		return r.json()['response']
	else:
		raise Exception(f"Request Error: {r.status_code}")


def id_query_dictionary(id):
	return {"q": f"id:{id}"}

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
			return f"reviewScore:[0 TO {val}]"
		elif dir == ">=":
			return f"reviewScore:[{val} TO *]"
		else:
			raise Exception("Bad direction value " + s)
