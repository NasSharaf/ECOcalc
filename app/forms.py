from flask_wtf import FlaskForm
from wtforms import IntegerField, FloatField, SubmitField
from wtforms.validators import DataRequired, Length
import ECOLib as eco

class PostForm(FlaskForm):
    motorSize = IntegerField('Motor Size', validators=[DataRequired()])
    motorEfficiency = FloatField('Motor Efficiency', validators=[DataRequired()])
    motorVoltage = IntegerField('Motor Voltage', validators=[DataRequired()])
    loadRPM = FloatField('motorEfficiency', validators=[DataRequired()])
    hoursOfUse = IntegerField('Say something', validators=[DataRequired()])
    motorKW = FloatField('motorEfficiency', validators=[DataRequired()])
    newMotorSize = IntegerField('Say something', validators=[DataRequired()])
    newmotorEfficiency = FloatField('motorEfficiency', validators=[DataRequired()])
    newmotorVoltage = IntegerField('Say something', validators=[DataRequired()])
    newloadRPM = FloatField('motorEfficiency', validators=[DataRequired()])
    newhoursOfUse = IntegerField('Say something', validators=[DataRequired()])
    newmotorKW = FloatField('motorEfficiency', validators=[DataRequired()])
    submit = SubmitField('Submit')