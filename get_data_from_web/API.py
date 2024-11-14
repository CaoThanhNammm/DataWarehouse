# ĐÂY LÀ LỚP LẤY RA CÁC HẰNG SỐ LIÊN QUAN ĐẾN CALL API
import configparser
from datetime import datetime
import general

def get_var_in_env(parent, child):
  config = configparser.ConfigParser()
  config.read('web.config', encoding='utf-8')
  return config.get(parent, child)

# lấy message của log table
def get_message(type):
  return get_var_in_env('message_log', type)

# lấy ra các loại status khác nhau
def get_type_waiting():
    return get_var_in_env('status_type', "waiting")

def get_type_running():
    return get_var_in_env('status_type', "running")

def get_type_failed():
    return get_var_in_env('status_type', "failed")

def get_type_complete():
    return get_var_in_env('status_type', "complete")

# lấy url mặc định của các table
def get_context_config():
  return get_var_in_env('context', 'url_control')

def get_context_log():
  return get_var_in_env('context', 'url_log')

def get_context_status():
  return get_var_in_env('context', 'url_status')

def get_context_bike():
  return get_var_in_env('context', 'url_bike')

def get_context_dateDim():
  return get_var_in_env('context', 'url_dateDim')

def get_context_email():
    return get_var_in_env('context', 'url_email')

def get_keyword_bike2school():
  return get_var_in_env('keyword', 'bike2school')

def get_keyword_xedapgiakho():
  return get_var_in_env('keyword', 'xedapgiakho')

def get_receiver_email():
  return get_var_in_env('receiver_email', 'email1')


def get_message_waiting():
    return get_var_in_env('message_for_email', 'waiting')

def get_message_running():
    return get_var_in_env('message_for_email', 'running')

def get_message_failed():
    return get_var_in_env('message_for_email', 'failed')

def get_message_complete():
    return get_var_in_env('message_for_email', 'complete')


def create_message_for_email(message):
    now = datetime.now()
    hour = now.hour
    minute = now.minute
    second = now.second

    message = f"""
    Ngày(YYYY/mm/dd): {general.get_local_date()}
    Thời gian: {hour}:{minute}:{second} 
    Trạng thái(WAITING): {message}
    """
    return message