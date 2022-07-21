from tasks import app, update_all_user_kucoin_account

REPEAT_EVERY = 30


@app.on_after_configure.connect
def schedule_periodic_tasks(sender, **kwargs):
    # Fetch and updating accounts of kucoin for all users every 30 seconds
    sender.add_periodic_task(REPEAT_EVERY, update_all_user_kucoin_account.s())
