from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer
##	from sklearn.linear_model import LogisticRegression
app = Flask(__name__)
model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def home():
	return render_template('home.html')
@app.route('/predict',methods=['POST'])
def predict():
	df= pd.read_csv("spam.csv", encoding="latin-1")
	df=df.drop(['Unnamed: 2', 'Unnamed: 3', 'Unnamed: 4'],axis=1)
	df=df.rename(columns={'v1':'label','v2': 'message'})
	df['label']=df.label.map({'spam':0, 'ham':1})
	# Features and Labels
	#df['label'] = df['class'].map({'ham': 0, 'spam': 1})
	X = df['message']
	##y = df['label']
	
	# Extract Feature With CountVectorizer
	cv = CountVectorizer()
	X = cv.fit_transform(X) # Fit the Data
	##from sklearn.model_selection import train_test_split
	##X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
	##	clf = LogisticRegression()
	##clf.fit(X_train,y_train)
	##clf.score(X_test,y_test)
	xp=""
	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = cv.transform(data).toarray()
		my_prediction = model.predict(vect)
		if my_prediction==1:
			xp="HAAM"
		else:
			xp="SPAAM"
	return render_template('home.html',prediction = xp)
if __name__ == '__main__':
	app.run(debug=True)
