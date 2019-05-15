import os
from flask import Flask, render_template, request, redirect, url_for

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
    @app.route('/<name>', methods['GET'])
    def index():
        return render_template('index.html', templatename=name)

    @app.route('/search',methods=['GET', 'POST'])
    def searchForm():
        form = ReviewSearchForm()
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

    @app.route('/lookup/<id>', methods=['GET'])
    def lookup(id):
        res = solr.id_search(id)
        if (int(res['numFound']) > 1):
            raise Exception(f"Found more than one document of ID {id}")
        iddoc = '' if int(res['numFound']) == 0 else res['docs'][0]
        return render_template('reviewdetail.html', id=id, doc=iddoc)

    return app
