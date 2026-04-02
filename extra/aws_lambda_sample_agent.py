import json
import boto3
import uuid

def lambda_handler(event, context):

    client = boto3.client('bedrock-agentcore', region_name='us-west-2')

    user_input = event.get('prompt', 'Tehran')
    payload = json.dumps({'topic': user_input})

    session_id = f"lambda_session_{str(uuid.uuid4()).replace('-','')}"

    print(f"Payload: {payload}, and session id: {session_id}")

    response = client.invoke_agent_runtime(
        agentRuntimeArn= 'arn:aws:bedrock-agentcore:us-west-2:811165582441:runtime/vacation_planner-inLPg4HMPl',
        payload= payload,
        qualifier= 'DEFAULT',
        runtimeSessionId = session_id
    )

    response_body = response.get('response').read()
    print(f"Response: {response_body}")

    response_data = json.loads(response_body)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'message': response_data,
            'session_id': session_id
        })
    }