import asyncio

async def echo(reader, writer):
    print(writer.get_extra_info('peername'))
    while not reader.at_eof():
        data = await reader.readline()
        # data = data.decode()
        print('lksdfjlkds', flush=True)
        command, args = data.split(max_split=1)
        # print(command)
        await writer.write(data.swapcase())
    writer.close()
    await writer.wait_closed()


# async def handler_loop(reader, writer):
#     while not reader.at_eof():
#         data = await reader.readline()
#         data = data.decode()
#         # print(data)
#         print(data.split())
#         command, args = data.split(max_split=1)
#         print(command, args)
#         if command == 'print':
#             writer.write(args.encode())
#         elif command == 'info':
#             args = args.strip()
#             if args == 'host':
#                 print(writer.get_extra_info('peername')[0])
#             elif args == 'port':
#                 print(writer.get_extra_info('peername')[1])
#     writer.close()
#     await writer.wait_closed()
            
                

async def main():
    server = await asyncio.start_server(echo, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())