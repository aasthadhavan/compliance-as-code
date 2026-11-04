import logging

logging.basicConfig(
    filename="logs/application.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def run_app():
    logging.info("Application started successfully")

if __name__ == "__main__":
    run_app()
