import flask
from models.Thread import Thread

def base_int_query(arg):
    param = flask.request.args.get(arg)
    if param:
        try:
            int_param = int(param)
        except:
            flask.abort(400, description="query parameter must be an integer")
        
        return int_param
    
    return None

def page_query(query, lim=10):
    page_num = base_int_query('pg')

    if not page_num:
        return query.limit(lim)
       
    if page_num < 1:
            flask.abort(400, description="query must be an integer greater than 0")

    return query.limit(lim).offset((page_num-1)*lim)