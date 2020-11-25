import flask
from models.Post import Post

def page_query(query, lim=2):
    page = flask.request.args.get('pg')
    if page:
        try:
            int_page = int(page)
        except:
            flask.abort(400, description='page number must be an integer greater than 0')

        if int_page < 1:
            flask.abort(400, description='page number must be an integer greater than 0')
            
        all_items = query.limit(lim).offset((int_page-1)*lim)
        
    else:
        all_items = query.limit(lim)
            
    return all_items