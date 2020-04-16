
from flask import Flask,request,render_template
from extractive_summarizer import text_summarizer


app=Flask(__name__)

@app.route("/")
def my_form():
    return render_template("index.html")

@app.route('/',methods=["POST"])
def my_form_post():
    try:
        text=request.form['u']
        output=text_summarizer(text)
        processed_output=output.output()
        return render_template("index.html",prediction_text=processed_output)
    except:
        return render_template("error.html")

if __name__=="__main__":
    app.run(debug=True)



