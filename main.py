from app import app

if __name__ == "__main__":
    app.debug = True #setting the debug mode to make error finding easier
    app.run() #run the entire flask application
