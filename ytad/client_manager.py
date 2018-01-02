import googleautoauth.client_manager
import googleautoauth.authorize

import ytad.config.authorization

def _get_client_credentials():
    credentials = \
        googleautoauth.authorize.build_client_credentials(
            client_id=ytad.config.authorization.GOOGLE_API_CLIENT_ID,
            client_secret=ytad.config.authorization.GOOGLE_API_CLIENT_SECRET)

    return credentials

def get_client_manager():
    """Return a CM instance. This requires
    GAA_GOOGLE_API_AUTHORIZATION_FILEPATH to be defined.
    """

    credentials = _get_client_credentials()

    cm = googleautoauth.client_manager.ClientManager(
            ytad.config.authorization.SERVICE_NAME,
            ytad.config.authorization.SERVICE_VERSION,
            credentials,
            ytad.config.authorization.API_SCOPES)

    return cm
