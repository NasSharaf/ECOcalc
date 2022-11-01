from flask import render_template, flash, redirect, url_for, request
from app import app
from app.forms import PostForm
from app.allECOS import allECOS
import ECOLib as eco 

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home', allFIMS=allECOS)

@app.route('/misc/<ecoCalc>', methods=['GET', 'POST'])
def ecoCalculation(ecoCalc):
    htmlForm = '/ECOForms/{}.html'.format(ecoCalc)
    myform = PostForm()
    if request.method == "POST":
       #store the form value
       print(request.form)
    if myform.validate_on_submit():
        flash('Submitted Motor Replacemnt info {}', myform)
        print('{}', myform)
        return redirect(url_for('index'))
    return render_template(htmlForm, title='Energy Efficient Motor Replacement', form=myform)

@app.route('/<ecoCalc>', methods=['GET', 'POST'])
def miscEcoCalculation(ecoCalc):
    htmlForm = 'form.html'
    dictECO = next(item for item in allECOS if item["link"] == ecoCalc)
    print(dictECO)
    myform = PostForm()
    if request.method == "POST":
       #store the form value
       print(request.form)
    return render_template(htmlForm, title=dictECO["title"], form=myform, attrs=dictECO["attributes"], assumptions=dictECO["assumptions"])
