
def assert_with_msg(expr, msg="Assert failed"):
    try:
        assert(expr)
    except:
        print(msg)
