import docker


from gateway.celery_app import celery_app


@celery_app.task
def test_solution():
    pass
