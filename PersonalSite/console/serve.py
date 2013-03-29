def serve(**kwargs):
    from PersonalSite import app
    host = kwargs.get('host')
    port = kwargs.get('port')
    app.run(host=host, port=port)