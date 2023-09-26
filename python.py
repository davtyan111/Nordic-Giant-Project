import requests

def send_slack_notification(message, status):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = {
        'text': message
    }

    if status:
        payload['text'] = f'Успешно: {message}'
    else:
        payload['text'] = f'Ошибка: {message}'

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print('Уведомление успешно отправлено в Slack')
    else:
        print(f'Произошла ошибка {response.status_code} при отправке уведомления в Slack')

# Пример использования при успешном завершении:
send_slack_notification('Деплоймент завершен успешно', True)

# Пример использования при ошибке:
send_slack_notification('Произошла ошибка при деплойменте', False)
