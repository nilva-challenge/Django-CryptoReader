def convert(tup) -> dict:
    """
    takes a tuple , generates the same as dictionary
    :param tup:
    :return:
    """
    di = {}
    for a, b in tup.items():
        di.setdefault(a, b)
    return di


def custom_filter(data: list, filter_params: dict, time_params: list = None) -> list:
    """

    :param data: raw orders with no filter
    :param filter_params: params and values in which we want to filter with , for instance : side=buy
    :param time_params: a list of start and end like this [2312315,1412412] to filter by timestamp
    :return: the filtered data
    """
    filtered = [x for x in data if not filter_params.items() - x.items()] if filter_params else data
    if time_params:
        filtered = [x for x in filtered if time_params[0] <= x['createdAt'] < time_params[1]]

    return filtered
