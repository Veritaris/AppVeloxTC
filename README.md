[![Coverage Status](https://coveralls.io/repos/github/Veritaris/AppVeloxTC/badge.svg?branch=develop)](https://coveralls.io/github/Veritaris/AppVeloxTC?branch=master)

Hi. This is a test case for AppVelox company to test my skills.
This is a simple flask based web-application to resize images.
I decided to user Nginx Unit instead of guinicorn+supervisor 'cause Unit can restart itself. Also, I suppose, Unit is code-friendly both to Python and Nginx, not only to Python.
deploy.sh have to be moved to ~ for Github Actions.