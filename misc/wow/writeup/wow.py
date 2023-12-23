import socket
import random
import os

W = 'You won!'
L = 'You lost!'

# Server detail
host = 'wow.knping.pl'
port = 20001



# do a bet and return the result win or lost, the balance and the number of times random is running
# it also to collect data by store the collected random value in data.txt
def betting(n):
    print('-'*5+'start'+'-'*5)
    print(f'You bet: {n}')
    bet = str(n)+'\n'
    s.sendall(bet.encode('utf-8'))

    # Receive and print the response
    response = s.recv(1024).decode('utf-8')
    
    #parse the response
    lines = response.split('\n')
    
    #extract result
    result = lines[-5]

    number_line = len(lines)
    number_of_random_running = number_line - 5

    # print result and number of random running
    print(f'server:{result}- {number_of_random_running}')

    #save the random value
    with open('data.txt', 'a') as file:
        for _ in range(number_of_random_running):
            file.write(lines[_].split(' ')[-1]+'\n')
        
    #extract user balance
    balance = lines[-4].split('=')[1]
    #print(f'Balance: {balance}')
    #print(response)
    print('-'*5+'end'+'-'*5)
    return result, int(balance), number_of_random_running

# do a bet and return the result win or lost, the balance and the number of times random is running
# this function is same as betting() but it does not collect data
def betting2(n):
    print('-'*5+'start'+'-'*5)
    print(f'You bet: {n}')
    bet = str(n)+'\n'
    s.sendall(bet.encode('utf-8'))

    # Receive and print the response
    response = s.recv(1024).decode('utf-8')
    

    #parse the response
    lines = response.split('\n')
    
    #extract result
    result = lines[-5]

    number_line = len(lines)
    number_of_random_running = number_line - 5

    # print result and number of random running
    print(f'server:{result}- {number_of_random_running}')

        
    #extract user balance
    balance = lines[-4].split('=')[1]
    #print(f'Balance: {balance}')
    print(response)
    print('-'*5+'end'+'-'*5)
    return result, int(balance), number_of_random_running

# brute force the seed with the collected data
def bruteforce():
    with open('data.txt') as f:
        results = f.read().split('\n')
        print(f"collected data length: {len(results)}")
    x=0

    for seed in range(1,10_000_001):
        random.seed(seed)
        j=-1
        while j<700:

            x=random.randint(1,100)
            j=j+1
            if x!= int(results[j]):
                #print(f'Wrong seed: {seed}')
                break

            while x!=1:
                x=random.randint(1,x)
                j=j+1
                if x!= int(results[j]):
                    #print(f'Wrong seed: {seed}')
                    break

        # we only check with 625 random value then break. It should be enough to have a correct seed
        if j>625:
            print(f'Correct seed: {seed}')
            correct_seed = seed
            break
    return correct_seed

# return the result win or lost at each round
def win_or_lose():
    
    x=random.randint(1,100)
    result = 1
    print(f'x: {result}- {x}')
    
    while x!=1:
        x=random.randint(1,x)
        result = result+1
        print(f'x: {result%2}- {x}')
    return result%2


################### Main program ##################

# remove the data.txt if it exists
try:
    os.remove('data.txt')
except:
    pass

# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((host, port))

    # Receive and print the welcome message
    welcome_message = s.recv(1024).decode('utf-8')
    #print(welcome_message)

    # Send 'y' to start the game
    s.sendall(b'y\n')

    # Receive and print the user and opponent balances
    balance_info = s.recv(1024).decode('utf-8')
    #print(balance_info)

    total_random = 0
    for i in range(150):
        print(f'Round: {i}')
        bet = 1
        result, balance, number_of_random_running = betting(bet)
        total_random = total_random + number_of_random_running
        
    print('Bruteforcing...')
    correct_seed = bruteforce()
    
    print(f'Correct seed: {correct_seed}')
    print('-'*20)

    random.seed(correct_seed)

    for _ in range(150):
        x=win_or_lose()
        print(f'Round {_}: {x}')
    
    print('Start cheating...')

    while int(balance)*2 <10_000_000:
        x = win_or_lose()
        if x == 1:
            bet = balance
            result, balance, number_of_random_running = betting2(bet)
            print(f'Simulate: You win ----> Betting: {result}')
        else:
            bet = 1
            result, balance, number_of_random_running = betting2(bet)
            print(f'Simulate: You lose ----> Betting: {result}')
    while True:
        x = win_or_lose()
        if x == 1:
            bet = 10_000_001-balance
            print('-'*5+'start'+'-'*5)
            print(f'You bet: {bet}')
            bet = str(bet)+'\n'
            s.sendall(bet.encode('utf-8'))
            

            # Receive and print the response
            response = s.recv(1024).decode('utf-8')
            print(response)
            break
        else:
            bet = 1
            result, balance, number_of_random_running = betting2(bet)
            print(f'Simulate: You lose ----> Betting: {result}')

    # Close the connection
    s.close()
    