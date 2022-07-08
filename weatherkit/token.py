# weatherkit/token.py
# A third-party library for Apple's WeatherKit API.
# Copyright 2022 David Kopec
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import jwt
from time import time
from dataclasses import dataclass


# A token data class that has the token itself as well as the expiry time.
@dataclass
class Token:
    token: str
    expiry: int


# Generate a JWT token for the weatherkit API
# *team_id* is the 10 digit Apple Developer team id
# *service_id* is the custom id you specified when you created the service.
# *key_id* is the 10 digit id associated with the private key.
# *key_path* is the path to a private key file.
# *expiry* is the number of seconds the token should be valid for.
# Returns a *Token*.
def generate_token(team_id: str, service_id: str, key_id: str, key_path: str, expiry: int) -> Token:
    with open(key_path, 'r') as key_file:
        key = key_file.read()
    current_time = int(time())
    expiry_time = current_time + expiry
    payload = {
        'iss': team_id,
        'iat': current_time,
        'exp': expiry_time,
        'sub': service_id
    }
    headers = {
        "kid": key_id,
        "id": f"{team_id}.{service_id}"
    }
    token = jwt.encode(payload, key, algorithm='ES256', headers=headers)
    return Token(token, expiry_time)

