# def pre_request(worker, req):
#     worker.log.debug("%s %s" % (req.method, req.path))


# def post_request(worker, req, environ, response):
#     worker.log.debug("%s" % (response.headers))
#     response.headers.append('Access-Control-Allow-Origin', '*')
#     response.headers.append('Access-Control-Allow-Headers',
#                             'Content-Type,Authorization')
#     response.headers.append('Access-Control-Allow-Methods',
#                             'GET,PUT,POST,DELETE,OPTIONS')
#     return response
