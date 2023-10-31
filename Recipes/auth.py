from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db, bcrypt
from . import model

bp = Blueprint("auth", __name__)