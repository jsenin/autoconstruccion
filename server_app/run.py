from autoconstruccion import create_app

application = create_app(config_name='DEVELOPMENT')

if __name__ == '__main__':
    application.run()
