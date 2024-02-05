#Implemented by Sandra.S
#Due 7th/04/2022
#This program performs similarly to the Task1.py program, however this time a checksum check is implemented. This is done to ensure that the packet
#which is recieved is complete and error-free.

#Imports the libraries needed for this program to work as intended.
import base64
import asyncio
import websockets
import json
import struct

#Defines the function compute_checksum.
def compute_checksum(source_port: int, dest_port: int, payload: bytearray):
    #Defines the checksum variable and gives it a value of 0.
    checksum = 0
    #Defines the length variable and gives it a value of 8 + length of the payload.
    length = 8 + len(payload)

    #These definitions convert the header fields into 2 byte values.
    sizeBytes = length.to_bytes(2, byteorder = 'little')
    sourceBytes = source_port.to_bytes(2, byteorder = 'little')
    destPortBytes = dest_port.to_bytes(2, byteorder = 'little')
    checksumBytes = checksum.to_bytes(2, byteorder = 'little')

    #All of the bytes are appended into a bytearray.
    packetTotal = sourceBytes + destPortBytes + sizeBytes + checksumBytes + payload

    #If the length of the packet is not a multiple of 2:
    if len(packetTotal) %2 != 0:
        #Add an extra zero byte onto the end of the packet, to make it even.
        packetTotal += struct.pack('!B', 0)

    #Iterating over the bytearray two bytes at a time:
    for i in range(0, length, 2):
        #Shifts all of the bytes in the packet to the left
        w = (packetTotal[i] << 8) + (packetTotal[i + 1])
        checksum += w

    #Performing the one's complement in order to complete the compiling of the checksum.
    checksum = (checksum >> 16) + (checksum & 0xFFFF)
    checksum = ~checksum & 0xFFFF
    return checksum

#Defines the asynchronous function get_Packet. This function recieves a packet from the server, decodes it and returns the decoded (and whole) packet.
async def get_Packet(websocket):
    #Waits until the packet from the server is recieved.
    packet = await websocket.recv()
    #Prints to console the encoded packet recieved from the server.
    print('Base 64:', packet)
    #Decodes the packet, using Base64.
    packet = base64.b64decode(packet)
    #Prints to console the Base64 decoded version of the packet.
    print('Server Sent:', packet)
    #Returns the packet, enabling the decode_Packet function to use it.
    return packet

#Defines the asynchronous function decode_Packet. This function breaks down the decoded packet into multiple different values and prints them to the console.
#Finally, the checksum is verified and prints the result of the verification to the console.
async def decode_Packet(websocket):
    #Waits for the get_Packet function to complete.
    packet = await get_Packet(websocket)
    print('Decoded Packet:')
    #Converts the first 2 header bytes in the packet into an integer that represents the source port.
    source_port = int.from_bytes(packet[0:2], 'little')
    #Prints the source port to the console.
    print('Source Port:', source_port)
    #Converts the next 2 header bytes in the packet into an integer that represents the destination port.
    dest_port = int.from_bytes(packet[2:4], 'little')
    #Prints the destination port to the console.
    print('Dest Port:', dest_port)
    #Converts the next 2 header bytes in the packet into an integer that represents the length of the data within the packet.
    dataLength = int.from_bytes(packet[4:6], 'little')
    #Prints the data length to the console.
    print('Data Length:', dataLength)
    #Converts the last 2 header bytes in the packet into an integer that represents the checksum of the packet.
    checksum = int.from_bytes(packet[6:8], 'little')
    #Prints the checksum to the console.
    print('Checksum:', checksum)
    #Begins at the eigth position within the packet. This traverses until the end of the packet in order to extract the payload.
    payload = packet[8:(dataLength+8)]
    #Begins at the eigth position within the packet. This traverses until the end of the packet in order to extract the payload.
    #The payload is then decoded using utf-8.
    decodedPayload = packet[8:(dataLength+8)].decode('utf-8')
    #Prints the payload to the console.
    print('Payload: ', decodedPayload)

    #Computes a checksum using the values provided from the decode_Packet function.
    checksumCheck = compute_checksum(source_port, dest_port, payload)
    #If the checksums match:
    if checksum == checksumCheck:
        #Awknowledge a valid checksum.
        print("Checksum Valid")
    else:
        #Awknowledge an invalid checksum.
        print("Checksum Invalid")

#Defines the asynchronous function main.
async def main():
    #Allocates which server should be connected to (localhost:5612).
    uri = "ws://localhost:5612"
    async with websockets.connect(uri) as websocket:
        #Waits for the decode_Packet function to complete.
        await decode_Packet(websocket)

#Runs the asynchronous function main().    
asyncio.run(main())
