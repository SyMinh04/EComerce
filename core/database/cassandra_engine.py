DATABASES = {
    'default': {
        'ENGINE': 'django_cassandra_engine',
        'NAME': 'stu_project',
        'HOST': '127.0.0.1',
        'PORT': 9042,
        'USER': 'hosyminh1182004',
        'PASSWORD': 'hosyminh1182004',
        'OPTIONS': {
            'replication': {
                'class': 'SimpleStrategy',
                'replication_factor': 1,
            },
            'connection': {
                'retry_connect': True,
                'consistency': 1,
            },
        },
    }
}
