import socket
import threading
import random

# Define IP address and port number
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 1234

# Define questions and answers
questions = ['What is the capital of France?', 'What is the largest planet in our solar system?', 'What is the smallest country in the world?']
answers = ['Paris', 'Jupiter', 'Vatican City']

# Create a TCP socket with IPv4 addressing
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((SERVER_HOST, SERVER_PORT))

# Listen for incoming connections
server_socket.listen()

# List to maintain connected clients
clients = []

def clientthread(client_socket):
    # Define client score
    score = 0
    
    # Send game instructions to the client
    instructions = 'Welcome to the quiz game! You will be asked random questions and you need to give the correct answer. Your score will be displayed after each question. Good luck!'
    client_socket.send(instructions.encode('utf-8'))
    
    while True:
        # Get a random question for the client
        index, question, answer = get_random_question_answer(client_socket)
        
        # Listen for client's answer
        try:
            data = client_socket.recv(1024).decode('utf-8').strip()
        except:
            # Remove client from the list if they cannot be reached
            clients.remove(client_socket)
            break
        
        # Check if the answer is correct
        if data.lower() == answer.lower():
            score += 1
            message = f'Correct! Your score is {score}.'
            client_socket.send(message.encode('utf-8'))
            # Remove the question from the list
            remove_question(index)
            # Get a new question for the client
            get_random_question_answer(client_socket)
        else:
            message = f'Incorrect. Your score is {score}.'
            client_socket.send(message.encode('utf-8'))
            # Remove the question from the list
            remove_question(index)
            # Get a new question for the client
            get_random_question_answer(client_socket)
    
    # Close the client socket
    client_socket.close()

def get_random_question_answer(client_socket):
    # Get a random index for the question
    index = random.randint(0, len(questions) - 1)
    question = questions[index]
    answer = answers[index]
    # Send the question to the client
    message = f'Question: {question}'
    client_socket.send(message.encode('utf-8'))
    return index, question, answer

def remove_question(index):
    # Remove the question and answer at the index
    questions.pop(index)
    answers.pop(index)

while True:
    # Accept incoming connections
    client_socket, client_address = server_socket.accept()
    print(f'New connection from {client_address}')
    
    # Add client to the list of clients
    clients.append(client_socket)
    
    # Start a new thread for the client
    threading.Thread(target=clientthread, args=(client_socket,)).start()
