################################################ Importing libraries #############################################

from flask import Flask,render_template,request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired,URL
from wtforms import ValidationError
from plotly.offline import plot
from plotly.graph_objs import Scatter
from flask import Markup
from keras.models import model_from_json
import matplotlib.pyplot as plt
import urllib.request
from PIL import Image
from numpy import asarray

##################################################################################################################
################################################# app config #####################################################

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

#################################################################################################################
############################################# Forms #############################################################

class Home(FlaskForm):
	link = StringField('paste the link here', validators=[DataRequired()])
	submit=SubmitField('Predict')
class Home2(FlaskForm):
	link2 = StringField('paste the link here', validators=[DataRequired()])
	submit2=SubmitField('Predict')

################################################################################################################

cdlink=''                    ###########################global variables########################################
global loaded_model
global loaded_model2

################################################################################################################
########################################################loading models##########################################
###############cats n dogs model#########
json_file = open('model81.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("model81.h5")
print("Loaded model from disk")
#########################################
##############landscapes model###########
json_file = open('model82t.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model2 = model_from_json(loaded_model_json)
loaded_model2.load_weights("model82t.h5")
print("Loaded model2 from disk")
#########################################
###############################################################################################################
#################################### opening image and applying model##########################################

def model(Model):
	url=cdlink                                                   
	image = Image.open(urllib.request.urlopen(url))
	if Model==loaded_model:
		image2=image.resize((64, 64))
		p=64
	else:
		image2=image.resize((128,128))
		p=128
	print(image2.mode)
	print(image2.size)
	plt.imshow(image2)
	print(asarray(image2).shape)
	plt.imshow(image2)
	X=Model.predict((asarray(image2)/255).reshape(1,p,p,3))
	print(X)
	return X

################################################################################################################
######################### views ################################################################################

@app.route('/catsndogs',methods=['GET','POST'])
def catsndogs():
	print(cdlink)
	X=model(loaded_model)
	my_plot_div = plot([Scatter(x=[1, 2, 3], y=[3, 1, 6])], output_type='div')
	lst=[]
	for i in X[0]:
		lst.append(i)
	return render_template('catsndogs.html',X=lst,cdlink=cdlink,div_placeholder=Markup(my_plot_div))
	#return render_template('catsndogs.html',cdlink=cdlink)

@app.route('/landscapes',methods=['GET','POST'])
def landscapes():
	print(cdlink)
	X=model(loaded_model2)
	lst=[]
	for i in X[0]:
		lst.append(i)
	return render_template('landscapes.html',X=lst,cdlink=cdlink)

@app.route('/',methods=['GET','POST'])
def index():
	form = Home()
	form2 = Home2()
	global cdlink
	if form.validate_on_submit():
		print('f'+form.link.data)
		cdlink=form.link.data
		print(cdlink)
		return redirect(url_for('catsndogs'))
	if form2.validate_on_submit():
		print(form2.link2.data)
		cdlink=form2.link2.data
		return redirect(url_for('landscapes'))
	output=''
	print('else part')
	return render_template('home.html',output=output,form=form,form2=form2)

################################################################################################################

############################serve###############################################################################

if __name__=='__main__':
	app.run(debug=True)

################################################################################################################