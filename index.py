import platform

from app import create_app

app = create_app()

if __name__ == '__main__':
    if platform.system() == "Linux":
        app.run(host="0.0.0.0", port=5001)
    else:
        app.run(host="0.0.0.0", port=5555, debug=True)
