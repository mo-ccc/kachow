from controllers.thread_controller import threads
from controllers.post_controller import posts
from controllers.user_controller import users
from controllers.auth_controller import auth
from controllers.attachment_controller import attachments

blueprints = [threads, posts, users, auth, attachments]