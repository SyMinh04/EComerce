import json



class AuthenticationError(Exception):
    error = None
    status_code = 400
    description = ''

    def __init__(self, description=None, uri=None, state=None, status_code=None, request=None):
        """
        @param description: A human-readable ASCII [USASCII] text providing
                            additional information, used to assist the client
                            developer in understanding the error that occurred.
                            Values for the "error_description" parameter
                            MUST NOT include characters outside the set
                            x20-21 / x23-5B / x5D-7E.

        @param uri: A URI identifying a human-readable web page with information
                    about the error, used to provide the client developer with
                    additional information about the error.  Values for the
                    "error_uri" parameter MUST conform to the URI- Reference
                    syntax, and thus MUST NOT include characters outside the set
                    x21 / x23-5B / x5D-7E.

        @param state: A CSRF protection value received from the client.

        @param status_code:

        @param request: OAuthlib request.
        """
        if description is not None:
            self.description = description

        message = '({}) {}'.format(self.error, self.description)
        if request:
            message += ' ' + repr(request)
        super().__init__(message)

        self.uri = uri
        self.state = state

        if status_code:
            self.status_code = status_code

        if request:
            self.redirect_uri = request.redirect_uri
            self.client_id = request.client_id
            self.scopes = request.scopes
            self.response_type = request.response_type
            self.response_mode = request.response_mode
            self.grant_type = request.grant_type
            if not state:
                self.state = request.state
        else:
            self.redirect_uri = None
            self.client_id = None
            self.scopes = None
            self.response_type = None
            self.response_mode = None
            self.grant_type = None

    # def in_uri(self, uri):
    #     fragment = self.response_mode == "fragment"
    #     return add_params_to_uri(uri, self.twotuples, fragment)

    @property
    def twotuples(self):
        error = [('error', self.error)]
        if self.description:
            error.append(('error_description', self.description))
        if self.uri:
            error.append(('error_uri', self.uri))
        if self.state:
            error.append(('state', self.state))
        return error

    # @property
    # def urlencoded(self):
    #     return urlencode(self.twotuples)

    @property
    def json(self):
        return json.dumps(dict(self.twotuples))

    @property
    def headers(self):
        if self.status_code == 401:
            authvalues = ['error="{}"'.format(self.error)]
            if self.description:
                authvalues.append('error_description="{}"'.format(self.description))
            if self.uri:
                authvalues.append('error_uri="{}"'.format(self.uri))
            return {"WWW-Authenticate": "Bearer " + ", ".join(authvalues)}
        return {}


class TokenExpiredError(AuthenticationError):
    error = 'token_expired'


class InsecureTransportError(AuthenticationError):
    error = 'insecure_transport'
    description = 'OAuth 2 MUST utilize https.'


class MismatchingStateError(AuthenticationError):
    error = 'mismatching_state'
    description = 'CSRF Warning! State not equal in request and response.'


class MissingCodeError(AuthenticationError):
    error = 'missing_code'


class MissingTokenError(AuthenticationError):
    error = 'missing_token'


class MissingTokenTypeError(AuthenticationError):
    error = 'missing_token_type'


class FatalClientError(AuthenticationError):
    """
    Errors during authorization where user should not be redirected back.

    If the request fails due to a missing, invalid, or mismatching
    redirection URI, or if the client identifier is missing or invalid,
    the authorization server SHOULD inform the resource owner of the
    error and MUST NOT automatically redirect the user-agent to the
    invalid redirection URI.

    Instead, the user should be informed of the error by the provider itself.
    """
    pass


class InvalidRequestFatalError(FatalClientError):
    """
    For fatal errors, the request is missing a required parameter, includes
    an invalid parameter value, includes a parameter more than once, or is
    otherwise malformed.
    """
    error = 'invalid_request'


class InvalidRedirectURIError(InvalidRequestFatalError):
    description = 'Invalid redirect URI.'


class MissingRedirectURIError(InvalidRequestFatalError):
    description = 'Missing redirect URI.'


class MismatchingRedirectURIError(InvalidRequestFatalError):
    description = 'Mismatching redirect URI.'


class InvalidClientIdError(InvalidRequestFatalError):
    description = 'Invalid client_id parameter value.'


class MissingClientIdError(InvalidRequestFatalError):
    description = 'Missing client_id parameter.'


class InvalidRequestError(AuthenticationError):
    """
    The request is missing a required parameter, includes an invalid
    parameter value, includes a parameter more than once, or is
    otherwise malformed.
    """
    error = 'invalid_request'


class MissingResponseTypeError(InvalidRequestError):
    description = 'Missing response_type parameter.'


class MissingCodeChallengeError(InvalidRequestError):
    """
    If the server requires Proof Key for Code Exchange (PKCE) by OAuth
    public clients and the client does not send the "code_challenge" in
    the request, the authorization endpoint MUST return the authorization
    error response with the "error" value set to "invalid_request".  The
    "error_description" or the response of "error_uri" SHOULD explain the
    nature of error, e.g., code challenge required.
    """
    description = 'Code challenge required.'


class MissingCodeVerifierError(InvalidRequestError):
    """
    The request to the token endpoint, when PKCE is enabled, has
    the parameter `code_verifier` REQUIRED.
    """
    description = 'Code verifier required.'


class AccessDeniedError(AuthenticationError):
    """
    The resource owner or authorization server denied the request.
    """
    error = 'access_denied'


class UnsupportedResponseTypeError(AuthenticationError):
    """
    The authorization server does not support obtaining an authorization
    code using this method.
    """
    error = 'unsupported_response_type'


class UnsupportedCodeChallengeMethodError(InvalidRequestError):
    """
    If the server supporting PKCE does not support the requested
    transformation, the authorization endpoint MUST return the
    authorization error response with "error" value set to
    "invalid_request".  The "error_description" or the response of
    "error_uri" SHOULD explain the nature of error, e.g., transform
    algorithm not supported.
    """
    description = 'Transform algorithm not supported.'


class InvalidScopeError(AuthenticationError):
    """
    The requested scope is invalid, unknown, or malformed, or
    exceeds the scope granted by the resource owner.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """
    error = 'invalid_scope'


class ServerError(AuthenticationError):
    """
    The authorization server encountered an unexpected condition that
    prevented it from fulfilling the request.  (This error code is needed
    because a 500 Internal Server Error HTTP status code cannot be returned
    to the client via a HTTP redirect.)
    """
    error = 'server_error'


class TemporarilyUnavailableError(AuthenticationError):
    """
    The authorization server is currently unable to handle the request
    due to a temporary overloading or maintenance of the server.
    (This error code is needed because a 503 Service Unavailable HTTP
    status code cannot be returned to the client via a HTTP redirect.)
    """
    error = 'temporarily_unavailable'


class InvalidClientError(FatalClientError):
    """
    Client authenticators failed (e.g. unknown client, no client
    authenticators included, or unsupported authenticators method).
    The authorization server MAY return an HTTP 401 (Unauthorized) status
    code to indicate which HTTP authenticators schemes are supported.
    If the client attempted to authenticate via the "Authorization" request
    header field, the authorization server MUST respond with an
    HTTP 401 (Unauthorized) status code, and include the "WWW-Authenticate"
    response header field matching the authenticators scheme used by the
    client.
    """
    error = 'invalid_client'
    status_code = 401


class InvalidGrantError(AuthenticationError):
    """
    The provided authorization grant (e.g. authorization code, resource
    owner credentials) or refresh token is invalid, expired, revoked, does
    not match the redirection URI used in the authorization request, or was
    issued to another client.

    https://tools.ietf.org/html/rfc6749#section-5.2
    """
    error = 'invalid_grant'
    status_code = 400


class UnauthorizedClientError(AuthenticationError):
    """
    The authenticated client is not authorized to use this authorization
    grant type.
    """
    error = 'unauthorized_client'


class UnsupportedGrantTypeError(AuthenticationError):
    """
    The authorization grant type is not supported by the authorization
    server.
    """
    error = 'unsupported_grant_type'


class UnsupportedTokenTypeError(AuthenticationError):
    """
    The authorization server does not support the hint of the
    presented token type.  I.e. the client tried to revoke an access token
    on a server not supporting this feature.
    """
    error = 'unsupported_token_type'


class InvalidTokenError(AuthenticationError):
    """
    The access token provided is expired, revoked, malformed, or
    invalid for other reasons.  The resource SHOULD respond with
    the HTTP 401 (Unauthorized) status code.  The client MAY
    request a new access token and retry the protected resource
    request.
    """
    error = 'invalid_token'
    status_code = 401
    description = ("The access token provided is expired, revoked, malformed, "
                   "or invalid for other reasons.")


class TokenNotFoundError(AuthenticationError):
    """
    The token provided is not existed.
    The resource SHOULD respond with the HTTP 401 (Unauthorized) status code.
    The client MAY request a new access token and retry the protected resource request.
    """
    error = 'invalid_token'
    status_code = 401
    description = ('The access token provided not existed.')


class InsufficientScopeError(AuthenticationError):
    """
    The request requires higher privileges than provided by the
    access token.  The resource server SHOULD respond with the HTTP
    403 (Forbidden) status code and MAY include the "scope"
    attribute with the scope necessary to access the protected
    resource.
    """
    error = 'insufficient_scope'
    status_code = 403
    description = ("The request requires higher privileges than provided by the access token.")


class ConsentRequired(AuthenticationError):
    """
    The Authorization Server requires End-User consent.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User consent.
    """
    error = 'consent_required'


class LoginRequired(AuthenticationError):
    """
    The Authorization Server requires End-User authenticators.

    This error MAY be returned when the prompt parameter value in the
    Authentication Request is none, but the Authentication Request cannot be
    completed without displaying a user interface for End-User authenticators.
    """
    error = 'login_required'


class CustomAuthenticationError(AuthenticationError):
    """
    This error is a placeholder for all custom errors not described by the RFC.
    Some of the popular OAuth2 providers are using custom errors.
    """
    def __init__(self, error, *args, **kwargs):
        self.error = error
        super().__init__(*args, **kwargs)


def raise_from_error(error, params=None):
    import inspect
    import sys
    kwargs = {
        'description': params.get('error_description'),
        'uri': params.get('error_uri'),
        'state': params.get('state')
    }
    for _, cls in inspect.getmembers(sys.modules[__name__], inspect.isclass):
        if cls.error == error:
            raise cls(**kwargs)
    raise CustomAuthenticationError(error=error, **kwargs)
