# TODO import things I'll need
from flask import Flask, render_template

app = Flask(__name__)

# TODO homepage

@app.route('/homepage')
def homepage():
    return render_template("Pages/homepage.html", title="Homepage - Edesia")

@app.route('/registration/<type_user>')
def registration(type_user):
    if type_user == "consumer":
        return render_template("Pages/reg_consumer.html")
    elif type_user == "supplier":
        return render_template("Pages/reg_supplier.html")

@app.route('/consumer')
def consumer():
    return render_template('Pages/profile_consumer.html')

@app.route('/farmer')
def farmer():
    return render_template('Pages/profile_supplier.html')

@app.route('/aboutUs')
def about_us():
    return render_template("Pages/aboutUs.html", title="About Us - Edesia")

@app.route('/test')
def test():
    return render_template("Components/test.html")

@app.route('/results')
def research():
    return render_template("Pages/research_result.html")

@app.route('/farmer_store')
def farmer_store():
    return render_template("Pages/farmer_store.html")

if __name__ == '__main__':
    app.run()
