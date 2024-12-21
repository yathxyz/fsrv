from http.server import HTTPServer, SimpleHTTPRequestHandler
import cgi
import os

class FileUploadHandler(SimpleHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={
                'REQUEST_METHOD': 'POST',
                'CONTENT_TYPE': self.headers['Content-Type'],
            }
        )

        # Get the file item
        fileitem = form['file']
        
        # Check if a file was uploaded
        if fileitem.filename:
            # Write the file to current directory
            with open(os.path.basename(fileitem.filename), 'wb') as f:
                f.write(fileitem.file.read())
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"File uploaded successfully")
        else:
            self.send_response(400)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b"No file was uploaded")

if __name__ == '__main__':
    server = HTTPServer(('0.0.0.0', 8080), FileUploadHandler)
    print('Starting server on port 8080...')
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print('\nShutting down...')
        server.server_close()