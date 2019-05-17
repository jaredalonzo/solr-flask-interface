import os
from flask import Flask, render_template, request, redirect, url_for

import reviews.solrinterface as solr
from reviews.forms import ReviewSearchForm

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/', methods=['GET'])
    @app.route('/<name>', methods=['GET'])
    def index(name=''):
        return render_template('index.html', templatename=name)

    @app.route('/search',methods=['GET', 'POST'])
    def searchForm():
        form = ReviewSearchForm()
        print(type(form))
        if request.method == 'GET':
            return render_template('reviewsearch.html', form=form)
        elif not form.validate():
            return render_template('reviewsearch.html', form=form)
        else:
            return redirect(url_for('searchResults',
                                    k=form.keywords.data,
                                    d=form.scoreDirection.data,
                                    t=form.scoreThreshold.data,
                                    start=0))

    @app.route('/search/results', methods=['GET', 'POST'])
    def searchResults():
        k = request.args.get('k')
        d = request.args.get('d')
        t = request.args.get('t')
        print("k: " + k)
        print("d: " + d)
        print("t: " + t)
        start = request.args.get('start')
        res = solr.review_search(k, d + " " + t, start=start)
        return render_template('searchResults.html',
                                results=res,
                                start=int(start),
                                k=k, d=d, t=t)


    @app.route('/lookup')
    def idLookup():
        id = request.args.get('id')
        res = solr.id_search(id)
        if int(res['numFound']) > 1:
            raise Exception("Found more than one document of ID")
        elif int(res['numFound']) == 0:
            doc = ''
        else:
            doc = res['docs'][0]
        return render_template('reviewdetail.html', id=id, doc=doc)

    return app
