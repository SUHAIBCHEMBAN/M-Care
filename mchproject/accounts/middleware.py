from django.shortcuts import redirect, render

class RestrictAdminUserInFrontend:
    """
    Middleware to restrict access for admin users in the frontend and regular users in the admin panel.

    This middleware checks the request path and user authentication status to determine
    whether to allow or restrict access. It redirects admin users trying to access the frontend
    to the admin panel and renders the home page for regular users trying to access the admin panel.

    Attributes:
    - get_response: The next middleware in the chain or the view function.
    """
    def __init__(self, get_response):
        """
        Initialize the middleware with the next middleware in the chain or the view function.

        Parameters:
        - get_response: The next middleware in the chain or the view function.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request.

        Parameters:
        - request: The incoming HTTP request.

        Returns:
        - The HTTP response generated by this middleware or the next middleware/view function.
        """
        # Check if the request is for the admin panel and the user is a regular user
        if request.path.startswith('/admin/') and not request.user.is_superuser and request.user.is_authenticated:
            return render(request, 'home.html')    

        # Check if the request is for the frontend and the user is an admin
        if not request.path.startswith('/admin/') and request.user.is_superuser and request.user.is_authenticated:
            return redirect('/admin/')                                        
        
        response = self.get_response(request)
        return response