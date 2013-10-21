#!/usr/bin/env python
 
import socket
import httplib
import gnupg

# This is to identify your user/pass to the IRC server so your bot can be masked
# Thought it was safer to have it on user input rather than hardcoded            
user = raw_input("enter user ")
secret = raw_input("enter password ")
path = raw_input("path to key " ) # when starting scripts enter the path to your privkey rather than hardcoding
# name of the bot, channel and irc network
botnick = raw_input("BOT NICKNAME ")
network = 'irc.freenode.net'
 
# irc protocol
port = 6667
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((network, port))
print irc.recv(4096)
 
# bot will identify to the IRC server and join desired channel
irc.send('NICK ' + botnick + '\r\n')
irc.send('USER vitebot vitebot vitebot:python IRC\r\n')
irc.send('nickserv identify ' + user + ' ' + secret+ '\r\n')

while True:   

    # Creating shortcut variables
    data = irc.recv(4096)
    find = data.find
    send = irc.send 
    print data
    
    # This fetches the nicks
    nick = data.split('!')[0]
    nick = nick.replace(':', ' ')
    nick = nick.replace(' ', '')
    nick = nick.strip(' \t\n\r')
    
    # remote auth
    def auth():
        # Retrieve the encrypted message
        conn = httplib.HTTPConnection("bitcoin-otc.com")
        conn.request("GET", "/otps/23F0DD1989AAC87E")
        r1 = conn.getresponse()
        print r1.status, r1.reason
        # one time OTC secretphrase
        otc = r1.read()
        conn.close()
        print otc
        # decrypt the message
        gpg = gnupg.GPG(gnupghome=path)
        decrypted_data = gpg.decrypt(otc, passphrase=secret)
        print decrypted_data
        # send message to user
        send(' PRIVMSG ' + user + ' : ' + str(decrypted_data) + '\r\n')
        
    # PING PONG with the IRC server to avoid getting booted
    if find('PING') != -1:
        send('PONG ' + data.split()[1] + '\r\n')
        print "PONG SENT"
        print data
            
    # Establishing bot behaviour
    elif find(':!' + botnick) != -1:
        if user == nick:
            send('PRIVMSG ' + user + ' : Hi\r\n')
            print "Hi SENT"
            print data
    elif find(':!auth ' + user) != -1:
        if user == nick:
            auth()
            
    # This will only let the user end the script via IRC    
    elif find('!quit') != -1:
        if user == nick:
            send(' PRIVMSG ' + user + ' : Good Bye\r\n')
            send('quit\r\n')
            print data
            quit()
