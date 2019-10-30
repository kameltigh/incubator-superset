from flask import request
from superset.utils import core as utils

def time_filter(default: Optional[str] = None) -> Optional[Any]:
    form_data = request.form.get("form_data")

    if isinstance(form_data, str):
        form_data = json.loads(form_data)
        extra_filters = form_data.get("extra_filters") or {}
        time_range = [f["val"] for f in extra_filters if f["col"] == "__time_range"]
        time_range = time_range[0] if time_range else None

        since, until = utils.get_since_until(time_range)
        time_format = '%Y-%m-%d %H:%M:%S'

        if not until:
            return '!= \'0001-01-01 00:00:00\''

        until = until.strftime(time_format)
        if not since:
            return '<= \'{}\''.format(until)
        since = since.strftime(time_format)
        return 'BETWEEN \'{}\' AND \'{}\''.format(since, until)
    return default

