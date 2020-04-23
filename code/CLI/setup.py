from setuptools import setup

setup(

    name= 'KidoCLI',
    version='1.0',
    py_modules=["kido"],
    install_requires=[
        "click",
        "requests"
    ],
    entry_points='''
        [console_scripts]
        kido=kido:cli
    
    '''


)