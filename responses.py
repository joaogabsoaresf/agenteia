from flask import Response
import json

def success_response(response):
    return Response(
        json.dumps({"status": "success", "response":response}),
        status=200,
        mimetype='application/json'
    )

def from_user_response():
    return Response(
        json.dumps({"status": "message sent from the user himself"}),
        status=200,
        mimetype='application/json'
    )

def not_authorized_response():
    return Response(
        json.dumps({"error": "Unauthorized"}),
        status=401,
        mimetype='application/json'
    )

def service_off_response():
    return Response(
        json.dumps({"error": "service off"}),
        status=503,
        mimetype='application/json'
    )