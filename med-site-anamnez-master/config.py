import os


class AppConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or (
        '562d44942c925ef05e1224a6c0bdcc96ba0347e686092d57fbcf1ffe9ccfefd8')
    debug = True
