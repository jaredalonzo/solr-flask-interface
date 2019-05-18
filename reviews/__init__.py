import os
from flask import Flask, render_template, request, redirect, url_for
from jinja2 import Template

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

    @app.context_processor
    def utility():
        def search_title(asin):
            res = solr.product_asin_search(asin)
            if int(res['numFound']) > 1:
                raise Exception('Found more than one document')
            elif int(res['numFound']) == 0:
                doc = ''
            else:
                doc = res['docs'][0]['title']
            return doc
        return dict(search_title=search_title)

    @app.route('/', methods=['GET'])
    @app.route('/<name>', methods=['GET'])
    def index(name=''):
        return render_template('index.html', templatename=name)

    @app.route('/search',methods=['GET', 'POST'])
    def search_form():
        form = ReviewSearchForm()
        print(type(form))
        if request.method == 'GET':
            return render_template('reviewsearch.html', form=form)
        elif not form.validate():
            return render_template('reviewsearch.html', form=form)
        else:
            return redirect(url_for('search_results',
                                    k=form.keywords.data,
                                    start=0))

    @app.route('/search/results', methods=['GET', 'POST'])
    def search_results():
        k = request.args.get('k')
        # d = request.args.get('d')
        # t = request.args.get('t')
        # print("d: " + d)
        # print("t: " + t)
        start = request.args.get('start')
        res = solr.review_search(k, start=start)
        return render_template('searchresults.html',
                                results=res,
                                start=int(start),
                                k=k)

    @app.route('/review')
    def review_lookup():
        id = request.args.get('id')
        res = solr.id_search(id)
        if int(res['numFound']) > 1:
            raise Exception('Found more than one document')
        elif int(res['numFound']) == 0:
            doc = ''
        else:
            doc = res['docs'][0]
        return render_template('reviewdetail.html', id=id, doc=doc)

    @app.route('/product')
    def product_lookup():
        asin = request.args.get('asin')
        res = solr.product_asin_search(asin)
        if int (res['numFound']) > 1:
            raise Exception('Found more than one document')
        elif int(res['numFound']) == 0:
            doc = ''
        else:
            doc = res['docs'][0]
        return render_template('productdetail.html', asin=asin, doc=doc)

    return app
