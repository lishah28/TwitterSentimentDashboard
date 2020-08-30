from flask import Flask, render_template
import main


app = Flask(__name__)

@app.route('/')
def index():
    auth = main.authenticate_app()
    api = main.API(auth)
    search_phrase = input("Search keyword: ")
    all_tweets = main.collect_tweets(search_phrase, api)
    df = main.create_dataframe(all_tweets)
    remove_words = ["https", "co", "com", search_phrase]
    #main.make_wordcloud(df, remove_words)
    return render_template("index.html", content = df['Text'])

if __name__ == "__main__":

    app.run(debug = True)
