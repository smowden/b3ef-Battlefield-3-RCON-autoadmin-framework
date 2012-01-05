#!/usr/local/bin/python
#created by DICE

from struct import *
import binascii
import socket
import sys
import shlex
import string
import threading
import md5
#import readline
import os
import logging


def EncodeHeader(isFromServer, isResponse, sequence):
	header = sequence & 0x3fffffff
	if isFromServer:
		header += 0x80000000
	if isResponse:
		header += 0x40000000
	return pack('<I', header)

def DecodeHeader(data):
    [header] = unpack('<I', data[0 : 4])
    return [header & 0x80000000, header & 0x40000000, header & 0x3fffffff]

def EncodeInt32(size):
	return pack('<I', size)

def DecodeInt32(data):
    if(len(data)>=4):
        return unpack('<I', data[0 : 4])[0]
    else:
        return 0

def EncodeWords(words):
	size = 0
	encodedWords = ''
	for word in words:
		strWord = str(word)
		encodedWords += EncodeInt32(len(strWord))
		encodedWords += strWord
		encodedWords += '\x00'
		size += len(strWord) + 5
	
	return size, encodedWords
	
def DecodeWords(size, data):
	numWords = DecodeInt32(data[0:])
	words = []
	offset = 0
	while offset < size:
		wordLen = DecodeInt32(data[offset : offset + 4])		
		word = data[offset + 4 : offset + 4 + wordLen]
		words.append(word)
		offset += wordLen + 5
		#print "word offset "+str(offset)

	return words

def EncodePacket(isFromServer, isResponse, sequence, words):
	encodedHeader = EncodeHeader(isFromServer, isResponse, sequence)
	encodedNumWords = EncodeInt32(len(words))
	[wordsSize, encodedWords] = EncodeWords(words)
	encodedSize = EncodeInt32(wordsSize + 12)
	return encodedHeader + encodedSize + encodedNumWords + encodedWords

# Decode a request or response packet
# Return format is:
# [isFromServer, isResponse, sequence, words]
# where
#	isFromServer = the command in this command/response packet pair originated on the server
#   isResponse = True if this is a response, False otherwise
#   sequence = sequence number
#   words = list of words
	
def DecodePacket(data):
	[isFromServer, isResponse, sequence] = DecodeHeader(data)
	wordsSize = DecodeInt32(data[4:8]) - 12
	words = DecodeWords(wordsSize, data[12:])
	return [isFromServer, isResponse, sequence, words]

###############################################################################

clientSequenceNr = 0

# Encode a request packet

def EncodeClientRequest(words):
	global clientSequenceNr
	packet = EncodePacket(False, False, clientSequenceNr, words)
	clientSequenceNr = (clientSequenceNr + 1) & 0x3fffffff
	return packet

# Encode a response packet
	
def EncodeClientResponse(sequence, words):
	return EncodePacket(False, True, sequence, words)

###################################################################################

# Display contents of packet in user-friendly format, useful for debugging purposes
	
def printPacket(packet):

	if (packet[0]):
		print "IsFromServer, ",
	else:
		print "IsFromClient, ",
	
	if (packet[1]):
		print "Response, ",
	else:
		print "Request, ",

	print "Sequence: " + str(packet[2]),

	if packet[3]:
		print " Words:",
		for word in packet[3]:
			print "\"" + word + "\"",

	print ""

###################################################################################

def generatePasswordHash(salt, password):
	m = md5.new()
	m.update(salt)
	m.update(password)
	return m.digest()


def connectAndAuthenticate(host, port, pw):
    port=int(port)
    loggingInst=logging.getLogger('')
    
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    loggingInst.info('Connecting to port: %s:%d...' % ( host, port ))
    serverSocket.connect( ( host, port ) )
    serverSocket.setblocking(1)

    if pw is not None:
        loggingInst.info('Logging in - 1: retrieving salt...')

        # Retrieve this connection's 'salt' (magic value used when encoding password) from server
        getPasswordSaltRequest = EncodeClientRequest( [ "login.hashed" ] )
        serverSocket.send(getPasswordSaltRequest)

        getPasswordSaltResponse = serverSocket.recv(4096)
        loggingInst.info((DecodePacket(getPasswordSaltResponse)))

        [isFromServer, isResponse, sequence, words] = DecodePacket(getPasswordSaltResponse)

        # if the server doesn't understand "login.hashed" command, abort
        if words[0] != "OK":
            return False

        loggingInst.info('Received salt: ' + words[1])

        # Given the salt and the password, combine them and compute hash value
        salt = words[1].decode("hex")
        passwordHash = generatePasswordHash(salt, pw)
        passwordHashHexString = string.upper(passwordHash.encode("hex"))

        loggingInst.info('Computed password hash: ' + passwordHashHexString)

        # Send password hash to server
        loggingInst.info('Logging in - 2: sending hash...')

        loginRequest = EncodeClientRequest( [ "login.hashed", passwordHashHexString ] )
        serverSocket.send(loginRequest)

        loginResponse = serverSocket.recv(4096)	
        loggingInst.info(DecodePacket(loginResponse))

        [isFromServer, isResponse, sequence, words] = DecodePacket(loginResponse)

        # if the server didn't like our password, abort
        if words[0] != "OK":
            return False

        return serverSocket