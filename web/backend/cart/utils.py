from .constants import (PICKPOINT_TO_CDEK_STATUS_CODE_MAPPING,
                        RUPOST_TO_CDEK_STATUS_CODE_MAPPING)


def pickpoint_to_cdek_code(code):
    return code
    #return PICKPOINT_TO_CDEK_STATUS_CODE_MAPPING[code]


def rupost_to_cdek_code(code):
    cdek_code = RUPOST_TO_CDEK_STATUS_CODE_MAPPING.get(str(code), None)
    if cdek_code is None:
        return code
    return cdek_code

