# Patrick Lenis, Paul Cvasa, Amalia Muresan
# Web Technologies Project (Onlyne Banking System)

from website import create_app # import website python package

app = create_app() # create app instance

# run the flask website
if __name__ == '__main__':
    app.run(debug=True)
