#!/usr/bin/python
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from os import curdir, sep
import os
import json
from urlparse import urlparse
try:
    from urllib import unquote
except ImportError:
    from urllib.parse import unquote

PORT_NUMBER = 8800


# This class will handles any incoming request from
# the browser
class myHandler(SimpleHTTPRequestHandler):

    # Handler for the GET requests
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"

        try:

            # check http url query value
            # http://127.0.0.1:8080/abc.json?comment=1234
            writeComment = False
            comment = ''
            updateTestDetails = ''
            readFileList = ''
            query = urlparse(self.path).query
            if query:
                query_components = dict(qc.split("=") for qc in query.split("&"))

                # if query_components.__contains__('comment'):
                # if query_components.has_key('comment'):
                if 'comment' in query_components:
                    writeComment = True
                    comment = query_components["comment"]
                if 'updateTestDetails' in query_components:
                    updateTestDetails = True
                    detailComment = query_components["updateTestDetails"]
                    testId = query_components["testId"]
                if 'readFile' in query_components:
                    readFileList = True
                    baseFolder = query_components["readFile"]

            if writeComment == True:
                # filename = curdir + sep + self.path
                filename = curdir + urlparse(self.path).path

                # read json file
                with open(filename, 'r') as f:
                    json_data = json.load(f)
                    f.close()

                # update comment and write file
                comment = unquote(comment)
                if comment == "null":
                    comment = "";
                with open(filename, 'w') as f:
                    json_data['comment'] = comment
                    json.dump(json_data, f)
                    f.close()

                # return http response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                return
            elif updateTestDetails == True:
                # filename = curdir + sep + self.path
                filename = curdir + urlparse(self.path).path

                # read json file
                with open(filename, 'r') as f:
                    json_data = json.load(f)
                    f.close()

                # update comment and write file
                comment = unquote(detailComment)
                if comment == "null":
                    comment = "";
                with open(filename, 'w') as f:
                    tests = json_data['testResults']

                    for testResult in tests:
                        if testResult['test_id'] == testId:
                            testResult['analysis_comment'] = comment
                            break

                    json.dump(json_data, f)
                    f.close()

                # return http response
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                return
            elif readFileList == True:



                jsonData = [];
                baseFolder = curdir + urlparse(self.path).path
                if os.path.isdir(baseFolder):

                    for fileInFolder in os.listdir(baseFolder):
                        if('_' in fileInFolder and '_trend' not in fileInFolder and ".DS_Store" not in fileInFolder):
                            index = fileInFolder.split('_')[len(fileInFolder.split('_'))-1]
                            jsonData.append({'id':index, 'path': urlparse(self.path).path+'/'+fileInFolder})

                filename = baseFolder + '/list'
                # read json file
                with open(filename, 'w+') as f:
                    str = json.dumps(jsonData)
                    f.write(str)
                    f.close()


                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                return
            else:
                return SimpleHTTPRequestHandler.do_GET(self)


        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    # Handler for the POST requests


try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()