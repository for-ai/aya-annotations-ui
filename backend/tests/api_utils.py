def responses_sameshape(d1, d2):
    """
    Returns True if d1 and d2 have the same shape, False otherwise.

    Recursively checks the shape of d1 and d2.
    """

    if isinstance(d1, dict):
        if isinstance(d2, dict):
            # then we have shapes to check
            return (
                d1.keys() == d2.keys()
                and
                # so the keys are all the same
                all(responses_sameshape(d1[k], d2[k]) for k in d1.keys())
            )
            # thus all values will be tested in the same way.
        else:
            return False  # d1 is a dict, but d2 isn't
    else:
        return not isinstance(d2, dict)  # if d2 is a dict, False, else True.
