import requests

username = input('Введите имя пользователя: ')
url = 'https://api.github.com/users/'+username+'/repos'
req = requests.get(url)

if req.ok:
    data = req.json()
    list_file = open(''+username+'_list.txt', 'w', encoding="utf-8")
    for i in range(0, len(data)):
        print(f"Имя репозитория: {data[i]['name']} \n Ссылка на репозиторий: {data[i]['svn_url']} \n")
        list_file.write(f"Имя репозитория: {data[i]['name']} \n Ссылка на репозиторий: {data[i]['svn_url']} \n")

list_file.close()