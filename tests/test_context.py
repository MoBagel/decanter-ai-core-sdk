# pylint: disable=redefined-builtin
"""Test related method and functionality of Context."""
import pytest
import responses

from corex import Context
from corex.corex_vars import CoreXStatus


def test_no_context(globals, corex):
    """Test calling coerx_api when no context created.

    CoreXAPI will call context.LOOP, check if every api has raises
    AttributeError with message "event loop is \'NoneType\'".
    """
    with pytest.raises(AttributeError, match=r'event loop is \'NoneType\''):
        corex.upload(file=globals['test_csv_file'])

    with pytest.raises(AttributeError, match=r'event loop is \'NoneType\''):
        corex.train(train_input=globals['train_input'])

    with pytest.raises(AttributeError, match=r'event loop is \'NoneType\''):
        corex.predict(
            predict_input=globals['predict_input'])


@responses.activate
def test_connection_fail(context_fixture):
    """Context exits from Python when meeting any RequestException."""
    with pytest.raises(SystemExit):
        context_fixture('RequestException')


@responses.activate
def test_auth_fail(context_fixture):
    """Context exits from Python when authorization failed."""
    with pytest.raises(SystemExit):
        context_fixture('AuthFailed')


@responses.activate
def test_stop_jobs(globals, urls, corex, mock_test_responses, context_fixture):
    """Context stops the jobs in the list passed by `Context.stop.jobs()`"""
    async def cancel():
        context.stop_jobs([datas[0], datas[2]])
        responses.add(
            responses.GET, urls('task', 'upload'),
            json={
                '_id': globals['upload'],
                'status': CoreXStatus.DONE,
                'result': {
                    '_id': globals['data']}
                },
            status=200,
            content_type='application/json')

    context = context_fixture('Healthy')
    mock_test_responses(task='upload', status=CoreXStatus.RUNNING)
    responses.add(
        responses.PUT, urls('stop', 'upload'),
        json={
            'message': 'task removed'
        },
        status=200,
        content_type='application/json')
    datas = []
    for i in range(3):
        data = corex.upload(file=globals['test_csv_file'], name=str(i))
        datas.append(data)

    cancel_task = Context.LOOP.create_task(cancel())
    Context.CORO_TASKS.append(cancel_task)
    context.run()

    assert datas[0].status == CoreXStatus.FAIL
    assert datas[2].status == CoreXStatus.FAIL
    assert datas[1].status == CoreXStatus.DONE


@responses.activate
def test_stop_all_jobs(
        globals, urls, corex, mock_test_responses, context_fixture):
    """Context stops all jobs in running or pending status."""
    async def cancel():
        context.stop_all_jobs()
        return

    context = context_fixture('Healthy')
    mock_test_responses(task='upload', status=CoreXStatus.RUNNING)
    responses.add(
        responses.PUT, urls('stop', 'upload'),
        json={
            'message': 'task removed'
        },
        status=200,
        content_type='application/json')

    datas = []
    for i in range(3):
        data = corex.upload(file=globals['test_csv_file'], name=str(i))
        datas.append(data)

    cancel_task = Context.LOOP.create_task(cancel())
    Context.CORO_TASKS.append(cancel_task)
    context.run()

    assert all(data.status == CoreXStatus.FAIL for data in datas)
