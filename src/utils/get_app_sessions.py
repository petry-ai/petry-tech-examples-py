from fastapi import Request


# Helper function to get the sessions
def get_app_sessions(request: Request):
    return request.app.state.sessions
