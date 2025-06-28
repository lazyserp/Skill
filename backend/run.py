import os
from app.routes import create_app

app = create_app()

# Explicitly set the template folder path to ensure templates load correctly
app.template_folder = os.path.join(os.path.dirname(__file__), 'app', 'templates')

if __name__ == "__main__":
    app.run(debug=True)