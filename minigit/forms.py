# -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField,\
        DateTimeField, SubmitField, SelectField, HiddenField, BooleanField, RecaptchaField
from flask.ext.wtf import Required, Length, EqualTo, Optional, NumberRange, Email,\
        ValidationError, URL
from flask.ext.wtf.html5 import IntegerField, EmailField
import re
from hashlib import sha512
from flamejam import app, models

############## VALIDATORS ####################

class Not(object):
    def __init__(self, call, message = None):
        self.call = call
        self.message = message

    def __call__(self, form, field):
        errored = False
        try:
            self.call(form, field)
        except ValidationError:
            # there was an error, so don't do anything
            errored = True

        if not errored:
            raise ValidationError(self.call.message if self.message == None else self.message)

class MatchesRegex(object):
    def __init__(self, regex, message = "This field matches the regex {0}"):
        self.regex = regex
        self.message = message

    def __call__(self, form, field):
        if re.search(self.regex, field.data):
            raise ValidationError(self.message.format(self.regex))

class UsernameExists(object):
    def __call__(self, form, field):
        u = models.User.query.filter_by(username = field.data).first()
        if not u:
            raise ValidationError("The username does not exist.")

class EmailExists(object):
    def __call__(self, form, field):
        e = models.User.query.filter_by(email = field.data).first()
        if not e:
            raise ValidationError("That email does not exist")

class LoginValidator(object):
    def __init__(self, pw_field, message_username = "The username or password is incorrect.", message_password = "The username or password is incorrect."):
        self.pw_field = pw_field
        self.message_username = message_username
        self.message_password = message_password

    def __call__(self, form, field):
        u = models.User.query.filter_by(username = field.data).first()
        if not u:
            raise ValidationError(self.message_username)
        elif u.password != sha512((form[self.pw_field].data+app.config['SECRET_KEY']).encode('utf-8')).hexdigest():
            raise ValidationError(self.message_password)

class UsernameValidator(object):
    def __init__(self, message_username = "The username is incorrect."):
        self.message_username = message_username

    def __call__(self, form, field):
        u = models.User.query.filter_by(username = field.data).first()
        if not u:
            raise ValidationError(self.message_username)

############## FORMS ####################

class UserLogin(Form):
    username = TextField("Username", validators=[LoginValidator("password")])
    password = PasswordField("Password", validators = [])

class UserRegistration(Form):
    username = TextField("Username", validators=[
        MatchesRegex("[^0-9a-zA-Z\-_]", "Your username contains invalid characters. Only use alphanumeric characters, dashes and underscores."),
        Not(UsernameExists(), message = "That username already exists."),
        Length(min=3, max=80, message="You have to enter a username of 3 to 80 characters length.")])
    password = PasswordField("Password", validators=[Length(min=8, message = "Please enter a password of at least 8 characters.")])
    password2 = PasswordField("Password, again", validators=[EqualTo("password", "Passwords do not match.")])
    email = EmailField("Email", validators=[
            Not(EmailExists(), message = "That email address is already in use."),
            Email(message = "The email address you entered is invalid.")])
    captcha = RecaptchaField()

class ResetPassword(Form):
    username = TextField("Username", validators=[UsernameValidator()])

class NewPassword(Form):
    password = PasswordField("Password", validators=[Length(min=8, message = "Please enter a password of at least 8 characters.")])
    password2 = PasswordField("Password, again", validators=[EqualTo("password", "Passwords do not match.")])

class VerifyForm(Form):
    pass

class JamDetailsForm(Form):
    title = TextField("Title", validators=[Required(), Length(max=128)])
    theme = TextField("Theme", validators=[Length(max=128)])
    team_limit = IntegerField("Team size limit", validators=[NumberRange(min = 0)])
    start_time = DateTimeField("Start time", format="%Y-%m-%d %H:%M", validators=[Required()])

    registration_duration = IntegerField("Registration duration", validators=[Required(), NumberRange(min = 0)], default = 14 * 24)
    packaging_duration = IntegerField("Packaging duration", validators=[Required(), NumberRange(min = 0)], default = 24)
    rating_duration = IntegerField("Rating duration", validators=[Required(), NumberRange(min = 0)], default = 24 * 5)
    duration = IntegerField("Duration", validators=[Required(), NumberRange(min = 0)], default = 24 * 2)

    description = TextAreaField("Description")
    restrictions = TextAreaField("Restrictions")

class SubmitEditGame(Form):
    title = TextField("Game title", validators=[Required(), Length(max=128)])
    description = TextAreaField("Description", validators=[Required()])

class GameAddScreenshot(Form):
    url = TextField("URL", validators = [Required(), URL()])
    caption = TextField("Caption", validators = [Required()])

class GameAddTeamMember(Form):
    username = TextField("Username:", validators = [Required(), UsernameExists()])

from models import game_package_type_string

class GameAddPackage(Form):
    url = TextField("URL", validators = [Required()])
    type = SelectField("Type", choices = [
        ("web",          game_package_type_string("web")),
        ("linux",        game_package_type_string("linux")),
        ("linux32",      game_package_type_string("linux32")),
        ("linux64",      game_package_type_string("linux64")),
        ("windows",      game_package_type_string("windows")),
        ("windows64",    game_package_type_string("windows64")),
        ("mac",          game_package_type_string("mac")),
        ("source",       game_package_type_string("source")),
        ("git",          game_package_type_string("git")),
        ("svn",          game_package_type_string("svn")),
        ("hg",           game_package_type_string("hg")),
        ("combi",        game_package_type_string("combi")),
        ("love",         game_package_type_string("love")),
        ("blender",      game_package_type_string("blender")),
        ("unknown",      game_package_type_string("unknown"))])

class RateGame(Form):
    game_id = HiddenField(validators = [Required(), NumberRange(min = 1)])
    score_gameplay = IntegerField("Gameplay rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_graphics = IntegerField("Graphics rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_audio = IntegerField("Audio rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_innovation = IntegerField("Innovation rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_story = IntegerField("Story rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_technical = IntegerField("Technical rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_controls = IntegerField("Controls rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    score_overall = IntegerField("Overall rating", validators=[Required(), NumberRange(min=1, max=10)], default = 5)
    note = TextField("Additional notes", validators=[Optional()])

class SkipRating(Form):
    game_id = HiddenField(validators = [Required(), NumberRange(min = 1)])
    reason = SelectField("Reason to skip", choices = [
        ("platform", "Platform not supported"),
        ("uninteresting", "Not interested"),
        ("crash", "Game crashed on start")
    ])

class WriteComment(Form):
    text = TextAreaField("Comment", validators=[Required(), Length(max=65535)])


class TeamFinderFilter(Form):
    need_programmer = BooleanField("Programmer", default = True)
    need_gamedesigner = BooleanField("Game Designer", default = True)
    need_2dartist = BooleanField("2D Artist", default = True)
    need_3dartist = BooleanField("3D Artist", default = True)
    need_composer = BooleanField("Composer", default = True)
    need_sounddesigner = BooleanField("Sound Designer", default = True)

    show_teamed = BooleanField("people with a team")
    show_empty = BooleanField("people w/o abilities set", default = True)

    order = SelectField("Sort by", choices = [
        ("abilities", "Ability match"),
        ("username", "Username"),
        ("location", "Location")
    ], default = "abilities")

class SettingsForm(Form):
    ability_programmer = BooleanField("Programming")
    ability_gamedesigner = BooleanField("Game Design")
    ability_2dartist = BooleanField("Graphics / 2D Art")
    ability_3dartist = BooleanField("Modelling / 3D Art")
    ability_composer = BooleanField("Composing")
    ability_sounddesigner = BooleanField("Sound Design")
    abilities_extra = TextField("Detailed abilities")
    location = TextField("Location")
    real_name = TextField("Real Name")
    about = TextAreaField("About me")
    website = TextField("Website / Blog")

    old_password = PasswordField("Old Password", validators=[Optional()])
    new_password = PasswordField("New Password", validators=[Optional(), Length(min=8, message = "Please enter a password of at least 8 characters.")])
    new_password2 = PasswordField("New Password, again", validators=[EqualTo("new_password", "Passwords do not match.")])

    email = EmailField("Email", validators=[Optional(), Email(message = "The email address you entered is invalid.")])

    pm_mode = SelectField("Allow PM", choices = [
        ("email", "show my address"),
        ("form", "use email form"),
        ("disabled", "disable email")
    ], default = "form")

    notify_new_jam = BooleanField("when a jam is announced")
    notify_jam_start = BooleanField("when a jam I participate in starts")
    notify_jam_finish = BooleanField("when a jam I participate in finishes")
    notify_game_comment = BooleanField("when someone comments on a game of mine")
    notify_team_changes = BooleanField("when another team member edits the team data")
    notify_game_changes = BooleanField("when another team member edits the game data")
    notify_team_invitation = BooleanField("when someone invites me to a team")

    notify_newsletter = BooleanField("send me newsletters")

class RegisterJamForm(Form):
    show_in_finder = BooleanField("Show me in the team finder")

class UnregisterJamForm(Form):
    confirm = BooleanField("I understand that, please unregister me", validators = [Required()])

class TeamSettingsForm(Form):
    name = TextField("Team Name", validators=[Required()])
    wip = TextField("Working on")
    livestreams = TextAreaField("Livestreams")
    irc = TextField("IRC Channel")

class InviteForm(Form):
    username = TextField("Username", validators=[Required()])

class DevlogForm(Form):
    title = TextField("Title", validators=[Required()])
    text = TextAreaField("Content", validators=[Required()])
