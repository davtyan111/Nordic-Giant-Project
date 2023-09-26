import requests

def send_slack_notification(message, status):
    if status:
        webhook_url = 'https://hooks.slack.com/services/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'
        payload = {
            'text': f'Успешно: {message}'
        }
    else:
        print(f'Деплоймент завершен с ошибкой: {message}')
        return

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print('Уведомление успешно отправлено в Slack')
    else:
        print(f'Произошла ошибка {response.status_code} при отправке уведомления в Slack')

# Пример использования при успешном завершении:
send_slack_notification('Деплоймент завершен успешно', True)

# Пример использования при ошибке:
send_slack_notification('Произошла ошибка при деплойменте', False)
