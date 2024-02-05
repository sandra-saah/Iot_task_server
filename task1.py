#Implemented by Sandra.S 21039366
#Due 7th/04/2022
#This program recieves a packet from a UWE server, decodes it as UDP, and then splits it into different sections.
#The product is a printout of the packet in its encoded form, combined with a printout of the different elements within the packet.


#Imports the libraries needed for this program to work as intended.
import base64
import asyncio
import websockets
import json

#Defines the asynchronous function get_Packet.
async def get_Packet(websocket):
    #Waits until the packet from the server is recieved.
    packet = await websocket.recv()
    #Prints to console the encoded packet recieved from the server.
    print('Base 64:', packet)
    #Decodes the packet, using Base64.
    packet = base64.b64decode(packet)
    #Prints to console the Base64 decoded version of the packet.
    print('Server Sent:', packet)
    print('Decoded Packet:')
    #Converts the first 2 header bytes in the packet into an integer that represents the source port.
    source = int.from_bytes(packet[0:2], 'little')
    #Prints the source port to the console.
    print('Source Port:', source)
    #Converts the next 2 header bytes in the packet into an integer that represents the destination port.
    destPort = int.from_bytes(packet[2:4], 'little')
    #Prints the destination port to the console.
    print('Dest Port:', destPort)
    #Converts the next 2 header bytes in the packet into an integer that represents the length of the data within the packet.
    dataLength = int.from_bytes(packet[4:6], 'little')
    #Prints the data length to the console.
    print('Data Length:', dataLength)
    #Converts the last 2 header bytes in the packet into an integer that represents the checksum of the packet.
    checksum = int.from_bytes(packet[6:8], 'little')
    #Prints the checksum to the console.
    print('Checksum:', checksum)
    #Begins at the eigth position within the packet. This traverses until the end of the packet in order to extract the payload.
    #The payload is then decoded using utf-8.
    payload = packet[8:(dataLength+8)].decode('utf-8')
    #Prints the payload to the console.
    print('Payload: ', payload)

#Defines the asynchronous function main.
async def main():
    #Allocates which server should be connected to (localhost:5612).
    uri = "ws://localhost:5612"
    async with websockets.connect(uri) as websocket:
        #Waits for the get_Packet function to complete.
        await get_Packet(websocket)
    
#Runs the asynchronous function main().
asyncio.run(main())
