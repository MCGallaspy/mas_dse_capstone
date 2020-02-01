import datetime

def value_or_missing(val):
    '''
    ISD values uses a string of 9s to indicate missing data.
    This method checks if the data is missing and returns None if it is,
    or the actual string if not
    '''
    nval = len(val)
    all_9s = "9"*nval
    signed_9s = "+" + "9" * (nval-1)
    missing = (val == all_9s) or (val == signed_9s)
    return None if missing else val

def parse_isd_line(line):
    '''
    Parses a NOAA isd line. Returns data as a dictionary.
    '''
    # Station data
    var_data_len = int(line[0:4])
    usaf_station_id = line[4:10]
    wban_station_id = line[10:15]
    date = value_or_missing(line[15:27])
    date = datetime.datetime.strptime(date, "%Y%m%d%H%M") if date is not None else None
    latitude = value_or_missing(line[28:34])
    latitude = float(latitude) / 1000.0 if latitude else None
    longitude = value_or_missing(line[34:41])
    longitude = float(longitude) / 1000.0 if longitude else None
    report_type = value_or_missing(line[41:46])
    elevation = value_or_missing(line[46:51])
    elevation = int(elevation) if elevation else None
    call_letters = value_or_missing(line[51:56])
    qc_process = value_or_missing(line[56:59])
    
    # Air temp
    air_temp_c = value_or_missing(line[87:92])
    air_temp_c = float(air_temp_c) / 10. if air_temp_c else None
    
    return {
        "var_data_len": var_data_len,
        "usaf_station_id": usaf_station_id,
        "wban_station_id": wban_station_id,
        "date": date,
        "latitude": latitude,
        "longitude": longitude,
        "report_type": report_type,
        "elevation_meters": elevation,
        "call_letters": call_letters,
        "qc_process": qc_process,
        "air_temp_c": air_temp_c,
    }