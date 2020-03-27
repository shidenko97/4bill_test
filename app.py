from flask import Flask, jsonify
from pymemcache.client import base

from config import Config


# Initiate Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initiate memcached client
client = base.Client((Config.MEMCACHED_HOST, Config.MEMCACHED_PORT))

LIMITS = Config.REQUEST_LIMITS


def get_cache_key(**kwargs) -> str:
    """
    Function that returns the transformed cache key
    :param kwargs: Params for transform
    :return: Transformed cache key
    :rtype: str
    """

    return "current_limit_{period}".format(**kwargs)


def get_spent(period: int) -> int:
    """
    Function that returns already spent sum in specified period
    :param period: Specified period
    :type period: int
    :return: Already spent sum in specified period
    :rtype: int
    """

    # Load data from memcached and convert to int, if exists otherwise return 0
    cached_value = client.get(get_cache_key(period=period))
    return int(cached_value.decode('utf8')) if cached_value else 0


def check_limit(period: int, limit: int, amount: int) -> bool:
    """
    Function that check limit exceeded with entered sum
    :param period: Specified period
    :type period: int
    :param limit: Limit for period
    :type limit: int
    :param amount: Entered sum
    :type amount: int
    :return: Is limit exceeded
    :rtype: bool
    """

    spent = get_spent(period)

    if (spent + amount) > limit:
        return True
    return False


def set_limit(period: int, amount: int):
    """
    Function that set or increment spent sum
    :param period: Specified period
    :type period: int
    :param amount: Entered sum
    :type amount: int
    """

    cache_key = get_cache_key(period=period)
    spent = get_spent(period)

    if not spent:
        client.set(cache_key, amount, period)
    else:
        client.incr(cache_key, amount)


@app.route("/request/<int:amount>", methods=["GET"])
def pay(amount: int):
    """
    This is the payment API with some limits of payment sum per seconds
    ---
    parameters:
      - name: amount
        in: path
        type: int
        required: true
        description: The payment sum
    responses:
      200:
        description: Operation status
        schema:
          id: awesome
          properties:
            result:
              type: string
              description: The operation result
              default: OK
            error:
              type: string
              description: Description of error
    """

    result = {"result": "OK"}

    # Check exceeded limits
    exceeded = list(
        filter(lambda limit: check_limit(*limit, amount), LIMITS.items())
    )

    if exceeded:
        # If any limit is exceeded - return error with names of those limits
        exceeded_keys = [str(limit[0]) for limit in exceeded]
        result = {
            "error": f"amount limit exceeded ({'/'.join(exceeded_keys)}sec)"
        }
    else:
        # Otherwise set/increment all limits
        for period in LIMITS.keys():
            set_limit(period, amount)

    return jsonify(result)


if __name__ == '__main__':
    app.run()
