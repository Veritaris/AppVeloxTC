![CI](https://github.com/Veritaris/AppVeloxTC/workflows/CI/badge.svg?branch=master)
[![Coverage Status](https://coveralls.io/repos/github/Veritaris/AppVeloxTC/badge.svg?branch=master)](https://coveralls.io/github/Veritaris/AppVeloxTC?branch=master)

This is a simple flask based web-application to resize images made with REST-api strategy.
I decided to use Nginx Unit instead of guinicorn+supervisor 'cause Unit can restart itself. Also, I suppose, Unit is code-friendly both to Python and Nginx, not only to Python.
deploy.sh have to be moved to ~ for GitHub Actions.
