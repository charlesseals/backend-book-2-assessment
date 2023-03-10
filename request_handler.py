from urllib.parse import urlparse, parse_qs
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from views import get_all_specieses, get_single_species, get_single_snake, get_all_snakes, create_snake, get_all_owners, get_single_owner

class HandleRequests(BaseHTTPRequestHandler):

    def parse_url(self, path):
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = []

        if url_components.query != '':
            query_params = url_components.query.split("&")

        resource = path_params[0]
        id = None

        try:
            id = int(path_params[1])
        except IndexError:
            pass  # No route parameter exists: /animals
        except ValueError:
            pass  # Request had trailing slash: /animals/

        return (resource, id, query_params)    # This is a Docstring it should be at the beginning of all classes and functions
    # It gives a description of the class or function
    # """Controls the functionality of any GET, PUT, POST, DELETE requests to the server
    # """

    # Here's a class function

    # Here's a method on the class that overrides the parent's method.
    # It handles any GET request.
    def do_GET(self):
        # self._set_headers(200)

        response = {}

        # Parse URL and store entire tuple in a variable
        parsed = self.parse_url(self.path)

        # If the path does not include a query parameter, continue with the original if block
        if '?' not in self.path:
            # (resource, id, query_params) = parsed
            (resource, id, query_params) = parsed

            success = False

            if resource == "species":
                success = True
                if id is not None:
                    response = get_single_species(id)
                else:
                    response = get_all_specieses()

            elif resource == "snakes":
                success = True
                if id is not None:
                    response = get_single_snake(id)
                else:
                    response = get_all_snakes(query_params)
            elif resource == "owners":
                success = True
                if id is not None:
                    response = get_single_owner(id)
                else:
                    response = get_all_owners()


            if response == "":
                self._set_headers(405)
                response = ""
            elif success:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ""



        else: # There is a ? in the path, run the query param functions
            (resource, query, query_params) = parsed

            # see if the query dictionary has an email key
            if resource == 'species':
                success = True
                response = get_all_specieses()

            elif resource == "snakes":
                success = True
                response = get_all_snakes(query_params)

    
            if success:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = ""


            # elif resource == 'location':
            #     response = get_species_by_location(query_params][0])


        self.wfile.write(json.dumps(response).encode())



    def do_POST(self):
        # self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)

        post_body = json.loads(post_body)

        (resource, id, query_params) = self.parse_url(self.path)

        # key_test = False
        new_resource = None

        if resource == "snakes":
            # new_resource = ""
            # if list(post_body.keys())[list(post_body.values()).index(post_body['name'])] == 'name' and list(post_body.keys())[list(post_body.values()).index(post_body['owner_id'])] == 'owner_id' and list(post_body.keys())[list(post_body.values()).index(post_body['species_id'])] == 'species_id' and list(post_body.keys())[list(post_body.values()).index(post_body['gender'])] == 'gender' and list(post_body.keys())[list(post_body.values()).index(post_body['color'])] == 'color':
                # key_test = True
            #     self._set_headers(201)
            #     new_resource = create_snake(post_body)
            # else:
            #     self._set_headers(400)
            #     new_resource = f"Missing {}"


            if len(post_body) <= 4:
                self._set_headers(400)
                if 'name' not in post_body:
                    new_resource = "Request Is Missing Required Property `name`"
                elif 'owner_id' not in post_body:
                    new_resource = "Request Is Missing Required Property `owner_id`"
                elif 'species_id' not in post_body:
                    new_resource = "Request Is Missing Required Property `species_id`"
                elif 'gender' not in post_body:
                    new_resource = "Request Is Missing Required Property `gender`"
                elif 'color' not in post_body:
                    new_resource = "Request Is Missing Required Property `color`"

            elif len(post_body) == 5:
                self._set_headers(201)
                new_resource = create_snake(post_body)

            elif len(post_body) >= 6:
                self._set_headers(400)
                new_resource = "Request Contains Too Many Properties"




        # Encode the new animal and send in response
        self.wfile.write(json.dumps(new_resource).encode())






























        

    def _set_headers(self, status):
        # Notice this Docstring also includes information about the arguments passed to the function
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    # Another method! This supports requests with the OPTIONS verb.
    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()


# This function is not inside the class. It is the starting
# point of this application.
def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
