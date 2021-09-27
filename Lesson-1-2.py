import requests

method = input('Введите метод: ')
url = 'https://api.vk.com/method/'+method+''
token_file = open('token.txt', 'r')
my_params = {
    'v': 5.131,
    'access_token': token_file.read()
}
req = requests.get(url, params=my_params)

if req.ok:
    data = req.json()
    response_file = open('response.txt', 'w', encoding="utf-8")
    response_file.write(f'{data} \n')
    response_file.close()
    print(f'{data} \n')
else:
    print('Проверьте разрешения и срок действия токена')

token_file.close()