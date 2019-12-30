def login():
    print('\n\nLogin System v1.0...')
    username = input('Username: ')
    password = input('Password: ')

    if username == 'admin':
        if password == 'admin':
            print('Welcome, admin!')
            return 0
        else:
            print('Wrong password...')
            return 1
    
    if username == 'gabriel':
        if password == 'secure_pass123':
            print('Welcome, Gabriel!')
            return 0
        else:
            print('Wrong password...')
            return 1
    
    if username == 'username':
        if password == 'password':
            print('Welcome, Username!')
            return 0
        else:
            print('Wrong password...')
            return 1
    
    else:
        print('Invalid username...')
        return 2


if __name__ == '__main__':
    try:
        while True:
            login()

    except KeyboardInterrupt:
        print('Exiting...')
        exit()
    