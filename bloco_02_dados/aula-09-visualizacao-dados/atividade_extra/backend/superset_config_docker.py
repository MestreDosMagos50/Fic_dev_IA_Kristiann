# Permitir iframe em aplicações externas
ENABLE_CORS = True
CORS_OPTIONS = {
 'supports_credentials': True,
 'allow_headers': ['*'],
 'resources': ['*'],
 'origins': ['*']
 }
HTTP_HEADERS = {'X-Frame-Options': 'ALLOWALL'}
FEATURE_FLAGS = {
 "EMBEDDED_SUPERSET": True
}
