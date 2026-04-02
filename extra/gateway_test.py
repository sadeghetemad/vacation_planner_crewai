import requests
import json

CLIENT_ID = "5do80s70tb5v607pigh1i1uleo"
CLIENT_SECRET = "kni0hfklc8m6fu26gofqs5ns88ba71mnk53dudblsid1cb6592q"
TOKEN_URL = "https://us-west-2eut9zw4rr.auth.us-west-2.amazoncognito.com/oauth2/token"

def fetch_access_token(client_id, client_secret, token_url):
  response = requests.post(
    token_url,
    data="grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}".format(client_id=client_id, client_secret=client_secret),
    headers={'Content-Type': 'application/x-www-form-urlencoded'}
  )
  print(f'Access Token: {response.json()['access_token']}')
  return response.json()['access_token']

def list_tools(gateway_url, access_token):
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"
  }

  payload = {
      "jsonrpc": "2.0",
      "id": "list-tools-request",
      "method": "tools/list"
  }

  response = requests.post(gateway_url, headers=headers, json=payload)
  return response.json()


def call_tool(gateway_url, access_token, tool_name, arguments):
  headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {access_token}"  
  }

  payload = {
      "jsonrpc": "2.0",
      "id": "call-tool-request",
      "method": "tools/call",
      "params": {
          "name": tool_name,      # Tool identifier
          "arguments": arguments # Input parameters for the tool
      }
  }

  response_tool = requests.post(gateway_url, headers=headers, json=payload)
  print("Travel Package Details:", response_tool.json())
  return response_tool.json()

# Example usage
gateway_url = "https://gateway-vacation-planner-tefjc6yepw.gateway.bedrock-agentcore.us-west-2.amazonaws.com/mcp"
access_token = fetch_access_token(CLIENT_ID, CLIENT_SECRET, TOKEN_URL)
tools = list_tools(gateway_url, access_token)
print(json.dumps(tools, indent=2))

# Call the travel packages tool
tool_response = call_tool(gateway_url, access_token, "traveltool___travel_package_detail_tool", {"city": "tehran"})
print(tool_response)