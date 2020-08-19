"""
The services module of this blueprint.
"""
import json
from urllib.request import urlopen

from flask import current_app
from jose import jwt
from jose.constants import ALGORITHMS
from jose.exceptions import JWTClaimsError, JWTError

from application.database import db
from application.hti.models import JwtId

JWT_VALIDATION_OPTIONS = {
    'require_aud': True,
    'require_exp': True,
    'require_iss': True,
    'require_jti': True}


class HtiLaunchService:
    """
    The HtiLaunchService is responsible form managing the HTI launches.
    """

    def launch(self, token: str, host: str):
        """
        The launch method is responsible for unpacking and validating the token.

        This implementation makes use of the jwks discovery to get the public key from
        the portal application. The HTI standard allows this, as it states that
        modules MAY make use of jwks discovery.

        If the portal do not support  jwks discovery, the module application should persist
        the public key associated with the issuer (iss) and look it up.

        The HtiPortalService is responsible for looking up the key in this implementation.
        :param token: the JWT token
        :param host: the own hostname
        :return: the HTI task encoded in the token
        """
        issuer, key = hti_portal_service.get_portal(token)
        decode = jwt.decode(token, key, options=JWT_VALIDATION_OPTIONS, audience=host, issuer=issuer)
        self.replay_detection(decode)
        task = decode['task']
        return task

    @staticmethod
    def replay_detection(decode):
        """
        This method prevents replay attacks by checking if the JWT ID has not been seen before.
        :param decode: the decoded token
        :return: None
        :except: JWTClaimsError if the JWT ID has already been seen.
        """
        jti = decode['jti']
        if jwt_model_service.exists_jti(jti):
            raise JWTClaimsError('The JWT ID is not valid (jti)')

        jwt_model_service.store_jti(jti)


class HtiPortalService:
    """
    The HtiPortalService is responsible for finding the public key of the portal
    application that has created the token. There are two ways to implement this:

    1. Store or configure the public key of the portal and retrieve it by the value of the issuer (iss).
    2. Make use of the jwks discovery mechanism.

    This reference implementation makes use of jwks discovery method.
    """

    def get_portal(self, token: str) -> (str, dict):
        """
        This method makes of of the jwks discovery mechanism. First it tries to get the issuer from
        the token, checks if the issuer is allowed, and if so, returns the associated public key.
        :param token: an encoded token
        :return: the issuer and public key, if any.
        :raises: JWTClaimsError if the issuer is not allowed
        """
        issuer = jwks_discovery_service.get_issuer(token)
        if self.is_allowed_issuer(issuer):
            key: dict = jwks_discovery_service.discover_public_key_with_jwks(token)
            if key is None:
                raise JWTError(f'Cannot discover the jwks at {jwks_discovery_service.get_jwks_url(token)}')
            return issuer, key

        raise JWTClaimsError(f'The issuer (iss) {issuer} is not allowed, please set the HTI_ALLOWED_PORTALS '
                             f'enironment value.')

    @staticmethod
    def is_allowed_issuer(issuer):
        """
        Checks if the configuration allows this issuer to
        :param issuer:
        :return:
        """
        allowed_portals = current_app.config['HTI_ALLOWED_PORTALS'].split(',')
        allowed_portals = {x.strip() for x in allowed_portals}
        return issuer in allowed_portals


class JwksDiscoveryService:
    """
    This service discovers the public key of a portal with the jwks discovery mechanism.
    The token is queried by https://<issuer domain>/.well-known/jwks.json
    """

    def discover_public_key_with_jwks(self, token: str) -> dict:
        """
        This method gets the public key with the JWKS discovery method.
        :param token: the encoded token.
        :return: the JWKS key if found, else none.
        """
        url = self.get_jwks_url(token)
        kid = self.get_kid(token)
        if kid is not None and url is not None:
            return self.get_jwks_by_kid(url, kid)
        return None

    def get_jwks_url(self, token: str):
        """
        Gets the JWKS URL based on the issuer (iss). The URL is composed as
        https://<issuer>/.well-known/jwks.json
        :param token: the encoded token.
        :return: an URL.
        """
        issuer: str = self.get_issuer(token)
        if issuer is not None:
            domain = issuer
            if not domain.startswith('http'):
                domain = f'https://{domain}'

            if not domain.endswith('/'):
                domain = f'{domain}/'

            return f'{domain}.well-known/jwks.json'
        return None

    @staticmethod
    def get_issuer(token: str) -> str:
        """
        Gets the issuer (iss) from the encoded token.
        :param token: the encoded token.
        :return: the issuer (iss) from the encoded token.
        """
        decode = jwt.get_unverified_claims(token)
        return decode['iss'] if 'iss' in decode else None

    @staticmethod
    def get_kid(token: str) -> str:
        """
        Gets the key id (kid) from the header of the encoded token.
        :param token: the encoded token.
        :return: the key id (kid) from the header of the encoded token.
        """
        header = jwt.get_unverified_header(token)
        return header['kid'] if 'kid' in header else None

    @staticmethod
    def get_jwks_by_kid(url: str, kid: str) -> dict:
        """
        Fetches the URL, parsed the JWKS json file and tries to find
        the public key by its id (kid).
        :param url: the JWKS URL.
        :param kid: the key id (kid) to look for.
        :return: the public key as dict.
        """
        data = json.loads(urlopen(url).read().decode('utf8'))
        for key in data['keys']:
            if key['kid'] == kid:
                if 'alg' not in key:
                    key['alg'] = ALGORITHMS.RS512
                return key
        return None


class JwtModelService:
    """
    Service responsible for persisting and checking JWT ID values.
    """

    @staticmethod
    def exists_jti(jti):
        """
        Checks if the JWT Id (JTI) exists in the datastore.
        :param jti:
        :return: True if the JTI exists.
        """
        with current_app.app_context():
            return JwtId.query.filter_by(id=jti).count() > 0

    @staticmethod
    def store_jti(jti):
        """
        Stores a JWT Id (JTI) in the datastore.
        :param jti: the JWT Id (JTI)
        """
        with current_app.app_context():
            jwt_id = JwtId(id=jti)
            db.session.add(jwt_id)
            db.session.commit()


hti_launch_service = HtiLaunchService()
hti_portal_service = HtiPortalService()
jwks_discovery_service = JwksDiscoveryService()
jwt_model_service = JwtModelService()
