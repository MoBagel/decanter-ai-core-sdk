# pylint: disable=redefined-builtin
# pylint: disable=too-many-arguments
"""Test related method and functionality of Experiemt."""
import asyncio

import responses
import pytest

from corex import Context, TrainInput, TrainTSInput,\
                  PredictInput, PredictTSInput
from corex.corex_vars import CoreXStatus

fail_conds = [(stat, res) for stat in CoreXStatus.FAIL_STATUS for res in [None, 'result']]
fail_conds.append((CoreXStatus.DONE, None))


def get_train_ts_input(data):
    """Return different train_input with different data"""
    return TrainTSInput(
                data=data, target='test',
                datetime_column='test',
                endogenous_features=['test'],
                forecast_horizon='test',
                gap='test', time_unit='test',
                regression_method='test',
                classification_method='test',
                max_window_for_feature_derivation='test')


@responses.activate
def test_exp_success(
        globals, corex, mock_test_responses, context_fixture):
    """Experiment gets the result and id from CoreXAPI.train()"""
    context = context_fixture('Healthy')
    mock_test_responses(task='train', status=CoreXStatus.DONE)

    exp = corex.train(globals['train_input'])
    context.run()

    assert exp.task.id == globals['train']
    assert exp.id == globals['exp']
    assert exp.status == CoreXStatus.DONE
    assert exp.result == globals['results']['train']


@responses.activate
@pytest.mark.parametrize('status, result', fail_conds)
def test_exp_fail(
        globals, corex, status, result, mock_test_responses, context_fixture):
    """Experiment fails when status and result create fail conditions."""
    context = context_fixture('Healthy')
    mock_test_responses(task='train', status=status, task_result=result)

    exp = corex.train(globals['train_input'])
    context.run()

    assert exp.task.id == globals['train']
    assert exp.id is None
    assert exp.status == status
    assert exp.result == result


@responses.activate
def test_exp_fail_by_data(
        globals, corex, context_fixture):
    """Experiment fails if required data fails."""
    context = context_fixture('Healthy')
    exp = corex.train(
        train_input=TrainInput(
            data=globals['fail_data'], target='test-target',
            algos=['test-algo']))

    context.run()

    assert exp.task.id is None
    assert exp.id is None
    assert exp.status == CoreXStatus.FAIL
    assert exp.result is None


@responses.activate
@pytest.mark.parametrize('status', [CoreXStatus.PENDING, CoreXStatus.RUNNING, CoreXStatus.FAIL])
def test_exp_stop(
        globals, urls, corex, status, mock_test_responses, context_fixture):
    """Experiment status is fail if stopped during pending, running, and fail
    status, remains if in done status. The prediction following will failed
    if Experiment failed.
    """
    async def cancel(exp):
        await asyncio.sleep(1)
        exp.stop()
        return

    context = context_fixture('Healthy')
    mock_test_responses(task='train', status=status)
    responses.add(
        responses.PUT, urls('stop', 'train'),
        json={
            'message': 'task removed'
        },
        status=200,
        content_type='application/json')

    exp = corex.train(globals['train_input'])

    pred_res = corex.predict(
        predict_input=PredictInput(data=globals['fine_data'], experiment=exp))
    cancel_task = Context.LOOP.create_task(cancel(exp))
    Context.CORO_TASKS.append(cancel_task)
    context.run()

    assert exp.status == CoreXStatus.FAIL
    assert pred_res.status == CoreXStatus.FAIL


@responses.activate
def test_exp_ts_success(
        globals, corex, mock_test_responses, context_fixture):
    """Time series Experiment getting the result and id
    from CoreXAPI.train_ts()"""
    context = context_fixture('Healthy')
    mock_test_responses(task='train_ts', status=CoreXStatus.DONE)

    exp = corex.train_ts(globals['train_ts_input'])
    context.run()

    assert exp.task.id == globals['train']
    assert exp.id == globals['exp']
    assert exp.status == CoreXStatus.DONE
    assert exp.result == globals['results']['train']


@responses.activate
@pytest.mark.parametrize('status, result', fail_conds)
def test_exp_ts_fail(
        globals, corex, status, result, mock_test_responses, context_fixture):
    """Time series Experiment fails when status and result create fail
    conditions."""
    context = context_fixture('Healthy')
    mock_test_responses(task='train_ts', status=status, task_result=result)

    exp = corex.train_ts(train_input=globals['train_ts_input'])
    context.run()

    assert exp.task.id == globals['train']
    assert exp.id is None
    assert exp.status == status
    assert exp.result == result


@responses.activate
def test_exp_ts_fail_by_data(
        globals, corex, context_fixture):
    """Time series Experiment fails if required data fails."""
    context = context_fixture('Healthy')

    train_ts_input = get_train_ts_input(globals['fail_data'])
    exp = corex.train_ts(train_ts_input)
    context.run()
    assert exp.task.id is None
    assert exp.id is None
    assert exp.status == CoreXStatus.FAIL
    assert exp.result is None


@responses.activate
@pytest.mark.parametrize('status', [CoreXStatus.PENDING, CoreXStatus.RUNNING, CoreXStatus.FAIL])
def test_exp_ts_stop(
        globals, urls, corex, status, mock_test_responses, context_fixture):
    """Time series Experiment status fails if stopped during pending, running,
    and fail status, remains if in done status. The prediction following will
    fail if Time series Experiment fails.
    """
    async def cancel(exp):
        await asyncio.sleep(1)
        exp.stop()
        return

    context = context_fixture('Healthy')
    mock_test_responses(task='train_ts', status=status)
    responses.add(
        responses.PUT, urls('stop', 'train'),
        json={
            'message': 'task removed'
        },
        status=200,
        content_type='application/json')

    exp = corex.train_ts(globals['train_ts_input'])

    pred_res = corex.predict_ts(
        predict_input=PredictTSInput(
            data=globals['fine_data'], experiment=exp))
    cancel_task = Context.LOOP.create_task(cancel(exp))
    Context.CORO_TASKS.append(cancel_task)
    context.run()

    assert exp.status == CoreXStatus.FAIL
    assert pred_res.status == CoreXStatus.FAIL
