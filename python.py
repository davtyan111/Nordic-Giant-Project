import subprocess
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

def run_application():
    process = subprocess.Popen(['python', 'python.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    while True:
        output = process.stdout.readline()
        error = process.stderr.readline()

        if output == '' and process.poll() is not None:
            break

        if output:
            print(output.strip())
            send_slack_notification(f'Вывод: {output.strip()}')

        if error:
            print(error.strip())
            send_slack_notification(f'Ошибка: {error.strip()}')

    rc = process.poll()
    return rc

if __name__ == '__main__':
    rc = run_application()

    if rc == 0:
        send_slack_notification('Процесс завершен успешно')
    else:
        send_slack_notification(f'Произошла ошибка, код возврата: {rc}')
