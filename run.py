import logging

from app import create_app

app = create_app()

if __name__ == '__main__':
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # Define the timestamp format
    )
    file_handler = logging.FileHandler('registration_events.log')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.run(debug=True)