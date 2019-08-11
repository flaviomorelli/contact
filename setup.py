from setuptools import setup

setup(
   name="contact",
   version="0.1",
   py_modules=["contact"],
   install_requires=[
       "Click",
   ],
   entry_points="""
        [console_scripts]
        contact=contact:cli
   """ 
)