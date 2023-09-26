import requests

def send_slack_notification(message):
    webhook_url = 'https://hooks.slack.com/services/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'
    payload = {
        'text': message
    }

    response = requests.post(webhook_url, json=payload)

    if response.status_code == 200:
        print('Уведомление успешно отправлено в Slack')
    else:
        print(f'Произошла ошибка {response.status_code} при отправке уведомления в Slack')

# Пример использования:
send_slack_notification('Ваше уведомление с помощью App Runner')
