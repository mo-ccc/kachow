import flask
from models.Post import Post

def page_query(model, lim=10):
    def inner_decorator(func):
        def wrapper(*args, **kwargs):
            page = flask.request.args.get('pg')
            if page:
                try:
                    int_page = int(page)
                except:
                    flask.abort(400, description='page number must be an integer greater than 0')

                if int_page < 1:
                    flask.abort(400, description='page number must be an integer greater than 0')
                    
                all_items = model.query.limit(lim).offset((int_page-1)*lim)
                
            else:
                all_items = model.query.limit(lim)
            
            kwargs["items"] = all_items
            return func(*args, **kwargs)
            
        wrapper.__name__ = func.__name__
        return wrapper
        
    return inner_decorator