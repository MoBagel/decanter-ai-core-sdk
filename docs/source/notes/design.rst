.. _design:


Design Notes
=================

If you are curious why Decanter AI Core SDK does certain things the way it does and not differently,
this section is for you.


Design Decisions
-----------------

When developer are using decanter's API, such as using upload api to upload a csv file.
It needs to start the upload by sending the upload request and keep updating the
status by keep sending the requests and recieving the responses from get task api. Its not
that convenient and it'll block other processes while waiting the task to be done, causing
a waste for decanter server, since it can process at most four tasks at a time.

In order to let user handling the tasks more efficiently and instinctively. There are
three main goals

1.  User need not be aware of the existence of API.
2.  User need not be aware of the task lifecycle.
3.  Nonblocking when running tasks that don't have dependencies relationship.
    (ex. Tasks of uploading train and test data don't depend on each other,
    making them run concurrently and asynchronously saves more time.)


Design Structure
-----------------

We mainly have three actions to do during training models:

-   Upload(`Task`) ⇒ DataUpload(`Job`)
-   Train ⇒ Experiment
-   Predict ⇒Predict Result

We structure the result we want to get as `Job` which will stores the
properties we wish to get easily. Ｗe let every corresponding actions be
a `Task` which will be executed by `Job` in order to get the result from it.


The relationship between :class:`~decanter.core.jobs.job.Job`
and :class:`~decanter.core.jobs.task.Task`

1.  Each `Job` has a `Task` and the `Job`'s mission is to execute
    the `Task` and wait for it until it's done.
2.  `Job`'s properties (or attributes) is the result of the `Task`.
3.  When every `Job` start to execute and get the result from `Task`,
    it needs to wait for all the `Job` in its jobs list to be done.

Ex. `PredictResult <Job>` must wait for `Experiment <Job>`
and `DataUpload <Job>` to be done.


How to do asynchronously?
~~~~~~~~~~~~~~~~~~~~~~~~~

Why need asynchronously? Since the decanter server can actually handle
upto 4 tasks running at once, if we do the job synchronously, we could
only do one task at a  time which is time-wasting.

Using :doc:`python:library/asyncio-task` in Python asyncio library.
We use ``await`` to handle the blocking problems. According to
`this passage <https://www.aeracode.org/2018/02/19/python-async-simplified/>`_.

"When you call ``await``, the function you're in gets suspended while whatever
you asked to wait on happens, and then when it's finished, the event loop will
wake the function up again and resume it from the await call, passing any
result out."

Therefore, coroutines that involves time-consuming calls such as calling APIs
or waiting for pre-requests `Job` to be done will be blocked and idle, and this
is the condition we can call ``await``. It'll block the currently running
coroutines and put onto the event loop's list of paused coroutines so something
else can be run.

In `Job` they're two blocking conditions:

1.  Waiting for undone pre-requests jobs: Call ``await asyncio.sleep()`` to
    suspend the current running coroutine and resume after few seconds. Means
    that ``Job.wait()`` check the jobs status every five second.
2.  Calling API: When calling ``self.update()`` the `Task` will fetch the
    result from decanter.core server, we use ``await`` to wait for the result,
    so it can run other coroutines while waiting for the response.

``Job.wait``:

.. code-block:: python

    # pesudo code of the coroutine Job.wait()
    async def wait(self):
        # check if all the jobs in list is done
        # if haven't call sleep to let other coroutine can be execute
        while not all self.jobs is done:
                await asyncio.sleep(5)

        # if there's jobs failed the coroutine fails to and no need to execute
        if not all self.jobs is success:
                return

        # start to execute task
        self.task.run()

        # keep update task result and Job properties by calling self.update
        # finshed when task is done
        while self.task.not_done():
            await self.update()
            await asyncio.sleep(5)

        # update the status of the Job
        # other jobs that waits for this can know that it's done
        self.status = self.task.status


Structure Flow Overview
~~~~~~~~~~~~~~~~~~~~~~~~~
When we create the client of CoreClient() ``client = CoreClient()`` we simply
create a `Job`. And its coroutines ``Job.wait()`` will be scheduled to
execute in the event loop.

.. figure:: ../images/flow_1.png

Notice that the event loop won't start to run until we call
``context.run()`` and each `Job` has its own `Task` waited to be finished.

.. figure:: ../images/flow_2.png

But each `Job`'s task has different timing to start, as the picture below.
Ex. exp needs to wait for train data to finish, and pred_res needs to
wait for test data and exp.

.. figure:: ../images/flow_3.png

When a `Job` is finished, it will set its ``is_done`` tag to true, and
leave the event loop.

.. figure:: ../images/flow_4.png

Since the `Job` that waits for other `Job`s will keep monitor its ``is_done``
tag, when it finds all of the `Job` it's waiting is done, it will start to run
its own `Task`.

.. figure:: ../images/flow_5.png

.. figure:: ../images/flow_6.png
