"""
Django settings for musicwebsite project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'v4c9k2zfi(y&s&a$awh*f76y3kjhbd#q0ko^yos+kvrz#maj2w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'simpleui',
    'django.contrib.auth',
    'django.contrib.sites',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'music.apps.MusicConfig',
    'userprofile',
    'password_reset',
    'comment',
    'taggit',
    'ckeditor',
    'mptt',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    # 添加需要的第三方登录
    'allauth.socialaccount.providers.github',

]
# 设置站点
SITE_ID = 1
# 登录成功后重定向地址
LOGIN_REDIRECT_URL = '/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'musicwebsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                # allauth 启动必须项
                'django.template.context_processors.request',
            ],
        },
    },
]

WSGI_APPLICATION = 'musicwebsite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT= os.path.join(BASE_DIR,'collected_static')

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

# SMTP服务器，改为你的邮箱的smtp!
EMAIL_HOST = 'smtp.qq.com'
# 邮箱
EMAIL_HOST_USER = '974160357@qq.com'
# 授权码
EMAIL_HOST_PASSWORD = 'vqscsiwrldtfbcji'
# 发送邮件的端口
EMAIL_PORT = 25
# 是否使用 TLS
EMAIL_USE_TLS = True
# 默认的发件人
DEFAULT_FROM_EMAIL = '974160357@qq.com'

# 媒体文件地址
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')


# 富文本编辑器配置
CKEDITOR_CONFIGS = {
    # django-ckeditor默认使用default配置
    'default': {
        # 编辑器宽度自适应
        'width':'auto',
        'height':'250px',
        # tab键转换空格数
        'tabSpaces': 4,
        # 工具栏风格
        'toolbar': 'Custom',
        # 中文
        'language':'zh-cn',
        # 工具栏按钮
        'toolbar_Custom': [
            # 表情 特殊字符
            ['Smiley', 'SpecialChar'],
            # 字体风格
            ['Styles', 'Format','RemoveFormat''Bold', 'Italic', 'Underline',
             'Blockquote','Strike', 'SpellChecker', 'Undo', 'Redo'],
            # 字体颜色
            ['TextColor', 'BGColor'],
            # 链接
            ['Link', 'Unlink'],
            # 列表
            ['NumberedList', 'BulletedList'],
            # 最大化
            ['Maximize'],
        ],
        # 加入代码块插件
        'extraPlugins': ','.join(['codesnippet']),
        # UI颜色十六进制数
        'uiColor':'#CCFFFF',
        # 表情文件,放在/venv/Lib/site-packages/ckeditor/ckeditor/plugins/smiley/images
        'smiley_images':['1.gif','2.gif','3.gif','4.gif','5.gif','6.gif','7.gif','8.gif','9.gif','10.gif',
                       '11.gif','12.gif','13.gif','14.gif','15.gif','16.gif','17.gif','18.gif','19.gif','20.gif',
                       '21.gif','22.gif','23.gif','24.gif','25.gif','26.gif','27.gif','28.gif','29.gif','30.gif',
                       '31.gif','32.gif','33.gif','34.gif','35.gif','36.gif','37.gif','38.gif','39.gif','40.gif',
                       '41.gif','42.gif','43.gif','54.gif','45.gif','46.gif','47.gif','48.gif','49.gif','50.gif',
                        '51.gif','52.gif','53.gif','54.gif','55.gif','56.gif','57.gif','58.gif','59.gif','60.gif',
                        '61.gif','62.gif','63.gif','64.gif','65.gif','66.gif','67.gif','68.gif','69.gif','70.gif',
                        '71.gif','72.gif','73.gif','74.gif','75.gif','76.gif','77.gif','78.gif','79.gif','80.gif',
                        '81.gif','82.gif','83.gif','84.gif','85.gif','86.gif','87.gif','88.gif','89.gif','90.gif',
                        '91.gif','92.gif','93.gif','94.gif','95.gif','96.gif','97.gif','98.gif','99.gif','90.gif',
                        '101.gif','102.gif','103.gif','104.gif','105.gif','106.gif','107.gif','108.gif','109.gif','110.gif',
                        '111.gif','112.gif','113.gif','114.gif','115.gif','116.gif','117.gif','118.gif','119.gif','111.gif',
                        '121.gif','122.gif','123.gif','124.gif','125.gif','126.gif','127.gif','128.gif','129.gif','130.gif',
                        '131.gif','132.gif',
                        'a_1.png','a_2.png','a_3.png','a_4.png','a_5.png','a_6.png','a_7.png','a_8.png','a_9.png','a_10.png',
                        'a_11.png','a_12.png','a_13.png','a_14.png','a_15.png','a_16.png','a_17.png','a_18.png','a_19.png','a_20.png'
                        'a_21.png','a_22.png','a_23.png','a_24.png','a_25.png','a_26.png','a_27.png','a_28.png','a_29.png','a_20.png',
                        'a_31.png','a_32.png','a_33.png','a_34.png','a_35.png','a_36.png','a_37.png','a_38.png','a_39.png','a_30.png',
                        'a_41.png','a_42.png','a_43.png','a_44.png','a_45.png','a_46.png','a_47.png','a_48.png','a_49.png','a_40.png',
                        'a_51.png','a_52.png','a_53.png','a_54.png','a_55.png','a_56.png','a_57.png','a_58.png','a_59.png','a_60.png',
                        'a_61.png','a_62.png','a_63.png','a_64.png','a_65.png','a_66.png','a_67.png','a_68.png','a_69.png','a_70.png',
                         'a_nico.png','a_OK.png','a_what.png'

        ],
        #控制行表情个数
        'smiley_columns':20,
    }

}
X_FRAME_OPTIONS = 'SAMEORIGIN'

AUTHENTICATION_BACKENDS = (
    # Django 后台可独立于 allauth 登录
    'django.contrib.auth.backends.ModelBackend',
    # 配置 allauth 独有的认证方法，如 email 登录
    'allauth.account.auth_backends.AuthenticationBackend',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}