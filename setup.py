# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
from pathlib import Path  # noqa E402


CURRENT_DIR = Path(__file__).parent

def get_long_description() -> str:
    readme_md = CURRENT_DIR / "README.md"
    if not readme_md.exists():
        return """
        LICHOIS: Labor, Immigration, Citizenship, and Occupational Health Integrated Service

        This package provides an integrated service for managing labor, immigration, citizenship,
        and occupational health processes. For more detailed information, please refer to the
        project's GitHub repository or contact the maintainers.

        GitHub: https://github.com/Work-Res/lichois
        """
    return readme_md.read_text(encoding="utf-8")

setup(
    name='lichois',
    version='0.1.0',
    author='Africort Investments',
    author_email='ckgathi@africortinvestmemts.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/Work-Res/lichois',
    license='GPL licence, see LICENCE',
    description='Labor, Immigration, Citizenship, and Occupational Health Integrated Service (LICHOIS).',
    long_description=get_long_description(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    keywords='django models fields forms admin',
    install_requires=[
        'django',
        'django[argon2]',
        'django-simple-history',
        'django-js-reverse',
        'django-debug-toolbar',
        'django-extensions',
        'python-dateutil',
        'docutils',
        'model_mommy',
        'Faker',
        'pytz',
        'arrow',
        'python-memcached',
        'pymysql',
        'tqdm',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
