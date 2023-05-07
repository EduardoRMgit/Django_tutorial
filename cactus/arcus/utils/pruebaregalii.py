from regalii.configuration import Configuration
from regalii.regaliator import Regaliator

config = Configuration(
    # Authentication settings
    '00c0d2159be9988bfb4d5fd36a6d97df',
    b'+8teRHyPKfD5N/EWiRxeWsaDwjtD+ybdgZ0yeo8PtEkhV03cEUFTYxUD6AshGXqfgm/WkNbL6LY+nyI7y9ifJw==',

    # API host settings
    'api.staging.arcusapi.com',
    timeout=30,
    use_ssl=True,

    # Proxy settings
    proxy_host=None,
    proxy_port=None,
    proxy_user=None,
    proxy_pass=None,

    # Version target
    version='3.2')

r = Regaliator(config)
response = r.biller.utilities()
print(response.__dict__)
