"""
The views module for the single page interface (spi).
"""
from flask import Blueprint, redirect, send_from_directory

# pylint: disable=W0612
from application.security import require_session_html


def create_blueprint() -> Blueprint:
    """
    Blueprint init method.
    :return: the Blueprint instance
    """
    blueprint = Blueprint(__name__.split('.')[-2], __name__, static_folder='static')

    @blueprint.route('/')
    def root():
        """
        Returns the index view and redirects to the index.page.
        :return:
        """
        return redirect('index.html')

    @blueprint.route('/index.html')
    @require_session_html
    def index():
        """
        The index page.
        :return: the index page.
        """
        return blueprint.send_static_file('index.html')

    @blueprint.route('/<int:code>.html')
    def error(code):
        """
        The index page.
        :return: the index page.
        """
        return blueprint.send_static_file(f'{code}.html'), code

    @blueprint.route('/css/<path:path>')
    def css(path):
        """
        The /css views
        :param path: the sub path of /css
        :return: the css file in /css
        """
        return send_from_directory(blueprint.static_folder, 'css/' + path)

    @blueprint.route('/js/<path:path>')
    def javascript(path):
        """
        The /js views
        :param path: the sub path of /js
        :return: the javascript files in /js
        """
        return send_from_directory(blueprint.static_folder, 'js/' + path)

    blueprint.error = error
    return blueprint
