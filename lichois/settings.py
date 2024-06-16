"""
Django settings for lichois project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
from datetime import timedelta
from pathlib import Path
import ldap
from django_auth_ldap.config import LDAPSearch, GroupOfNamesType, PosixGroupType

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-dmfjvzo)p997$m)2fn&(zw$l8o%=#w=)q(_bs23v@f=qh$6u8r"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
	"django.contrib.admin",
	"django.contrib.auth",
	"django.contrib.contenttypes",
	"django.contrib.sessions",
	"django.contrib.messages",
	"whitenoise.runserver_nostatic",
	"django.contrib.staticfiles",
	"base_module.apps.AppConfig",
	"app.apps.AppConfig",
	"board.apps.AppConfig",
	"app_search.apps.AppSearchConfig",
	"app_pdf_utilities.apps.AppPdfUtilitiesConfig",
	"app_checklist.apps.AppChecklistConfig",
	"app_attachments.apps.AppAttachmentsConfig",
	"app_address.apps.AppAddressConfig",
	"app_contact.apps.AppContactConfig",
	"app_personal_details.apps.AppPersonalDetailsConfig",
	"app_comments.apps.AppCommentsConfig",
	"app_decision.apps.AppDecisionConfig",
	"app_assessment.apps.AppAssessmentConfig",
	"travel.apps.TravelConfig",
	"workresidentpermit.apps.WorkresidentpermitConfig",
	"workflow.apps.WorkflowConfig",
	"identifier.apps.AppConfig",
	"haystack",
	"rules.apps.AutodiscoverRulesConfig",
	"rest_framework",
	"rest_framework_swagger",
	'rest_framework.authtoken',
	'rest_framework_simplejwt',
	"viewflow",
	"viewflow.workflow",
	"django_filters",
	"django_api_client",
	"corsheaders",
	"django_extensions",
	"lichois",
	'django_roles_access',
	'authentication.apps.AppConfig',
	'django_otp',
	'drf_yasg',
	'django_q',
]

MIDDLEWARE = [
	"django.middleware.security.SecurityMiddleware",
	"whitenoise.middleware.WhiteNoiseMiddleware",
	"django.contrib.sessions.middleware.SessionMiddleware",
	"corsheaders.middleware.CorsMiddleware",
	"django.middleware.common.CommonMiddleware",
	"django.middleware.csrf.CsrfViewMiddleware",
	"django.contrib.auth.middleware.AuthenticationMiddleware",
	"django.contrib.messages.middleware.MessageMiddleware",
	"django.middleware.clickjacking.XFrameOptionsMiddleware",
	'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = "lichois.urls"

TEMPLATES = [
	{
		"BACKEND": "django.template.backends.django.DjangoTemplates",
		"DIRS": [],
		"APP_DIRS": True,
		"OPTIONS": {
			"context_processors": [
				"django.template.context_processors.debug",
				"django.template.context_processors.request",
				"django.contrib.auth.context_processors.auth",
				"django.contrib.messages.context_processors.messages",
			],
		},
	},
]

WSGI_APPLICATION = "lichois.wsgi.application"

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
	"default": {
		"ENGINE": "django.db.backends.sqlite3",
		"NAME": BASE_DIR / "db.sqlite3",
	}
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'lichois',
#         'USER': 'postgres',
#         'PASSWORD': 'cc3721b',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
	{
		"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
	},
	{
		"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
	},
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

AUTH_LDAP_ALWAYS_UPDATE_USER = True
AUTH_LDAP_FIND_GROUP_PERMS = True
AUTH_LDAP_CACHE_TIMEOUT = 3600

AUTH_LDAP_SERVER_URI = 'ldap://138.68.175.109:389'
AUTH_LDAP_BIND_DN = 'cn=admin,dc=africort,dc=com'
AUTH_LDAP_BIND_PASSWORD = 'africort@321'
AUTH_LDAP_USER_SEARCH = LDAPSearch('dc=africort,dc=com', ldap.SCOPE_SUBTREE, '(uid=%(user)s)')
AUTH_LDAP_GROUP_SEARCH = LDAPSearch('dc=africort,dc=com', ldap.SCOPE_SUBTREE, '(objectClass=posixGroup)')
AUTH_LDAP_GROUP_TYPE = PosixGroupType(name_attr="cn")
AUTH_LDAP_MIRROR_GROUPS = True
# AUTH_LDAP_START_TLS = True

# Populate the Django user from the LDAP directory.
AUTH_LDAP_REQUIRE_GROUP = "cn=active,ou=groups,dc=africort,dc=com"
AUTH_LDAP_DENY_GROUP = "cn=disabled,ou=groups,dc=africort,dc=com"

AUTH_LDAP_USER_ATTR_MAP = {
	"first_name": "givenName",
	"last_name": "sn",
	"email": "mail",
	"username": "uid",
	"password": "userPassword",
}
AUTH_LDAP_PROFILE_ATTR_MAP = {
	"home_directory": "homeDirectory"
}
AUTH_LDAP_USER_FLAGS_BY_GROUP = {
	"is_active": "cn=active,ou=groups,dc=africort,dc=com",
	"is_staff": "cn=staff,ou=groups,dc=africort,dc=com",
	"is_superuser": "cn=superuser,ou=groups,dc=africort,dc=com",
	"verification_1": "cn=Verification,ou=groups,dc=africort,dc=com"
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static', ]

STORAGES = {
	"staticfiles": {
		"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
	},
}

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
PDF_FOLDER = 'generated'
PDF_TEMPLATE_WORKRESIDENTPERMIT = "pdf/application_summary.html"
DEPARTMENT = "ministry of Citizen and industry"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.solr_backend.SolrEngine',
		'URL': 'http://127.0.0.1:8983/solr/app',
		'ADMIN_URL': 'http://127.0.0.1:8983/solr/admin/cores',
		'TIMEOUT': 60 * 5
	},
}

REST_FRAMEWORK = {
	'DEFAULT_FILTER_BACKENDS': [
		'django_filters.rest_framework.DjangoFilterBackend',
		'rest_framework.filters.OrderingFilter'
	],
	'DEFAULT_PERMISSION_CLASSES': (
		'rest_framework.permissions.IsAuthenticated',
	),
	'DEFAULT_AUTHENTICATION_CLASSES': (
		'rest_framework_simplejwt.authentication.JWTAuthentication',
		'rest_framework.authentication.SessionAuthentication',
		'rest_framework.authentication.BasicAuthentication',
	),
}


AUTHENTICATION_BACKENDS = (
	# 'django_auth_ldap.backend.LDAPBackend',
	'django.contrib.auth.backends.ModelBackend',
	'rules.permissions.ObjectPermissionBackend',
)

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'formatters': {
		'standard': {
			'format': '%(asctime)s %(levelname)s %(name)s %(message)s'
		}
	},
	'handlers': {
		'console': {
			'level': 'INFO',
			'class': 'logging.StreamHandler',
			'formatter': 'standard',
			'filters': []
		}
	},
	'loggers': {
		logger_name: {
			'level': 'WARNING',
			'propagate': True,
			'handlers': ["console"]
		} for logger_name in ['django', 'django.request', 'django.db.backends', 'django.template', 'app', 'workflow',
		                      'app_pdf_utilities', 'workresidentpermit', 'app_assessment']
	}
}

HAYSTACK_DOCUMENT_FIELD = "text"
HAYSTACK_ID_FIELD = "id"
# HAYSTACK_SIGNAL_PROCESSOR = "haystack.signals.RealtimeSignalProcessor"
AUTH_USER_MODEL = 'authentication.User'
CSRF_TRUSTED_ORIGINS = ['http://138.68.175.109:5173']
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "UPDATE_LAST_LOGIN": False,

    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": "",
    "AUDIENCE": None,
    "ISSUER": None,
    "JSON_ENCODER": None,
    "JWK_URL": None,
    "LEEWAY": 0,

    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",

    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",

    "JTI_CLAIM": "jti",

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=120),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),

    "TOKEN_OBTAIN_SERIALIZER": "authentication.serializers.TokenObtainPairSerializer",
    "TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSerializer",
    "TOKEN_VERIFY_SERIALIZER": "rest_framework_simplejwt.serializers.TokenVerifySerializer",
    "TOKEN_BLACKLIST_SERIALIZER": "rest_framework_simplejwt.serializers.TokenBlacklistSerializer",
    "SLIDING_TOKEN_OBTAIN_SERIALIZER": "rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer",
    "SLIDING_TOKEN_REFRESH_SERIALIZER": "rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer",
}

MS_APP_ID = '545afb37-aadb-45ba-9547-0da1be4ec597'
MS_TENANT_ID = 'd11d44f9-972d-4ae1-9c77-092a048d2a2e'
MS_CLIENT_SECRET = 'qyY8Q~69zc.DdI4rIzmNqG3shulaobgjakRe0aWT'
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

AAD_TENANT_ID = "d11d44f9-972d-4ae1-9c77-092a048d2a2e"
AAD_CLIENT_ID = "545afb37-aadb-45ba-9547-0da1be4ec597"
AAD_CLIENT_SECRET = "qyY8Q~69zc.DdI4rIzmNqG3shulaobgjakRe0aWT"

Q_CLUSTER = {
    'name': 'lichois',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0, }
}
