from flask_internals import create_app

"""Start the actual application"""
app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0')