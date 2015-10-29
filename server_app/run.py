from autoconstruccion import create_app, create_db

application = create_app()

# Create database
create_db()


if __name__ == '__main__':
    application.run()
