import asyncio
import json
import logging

logging.basicConfig(filename='server.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

async def handle_client(reader, writer):
    # Read the request from the client
    request_data = await reader.read()
    request = json.loads(request_data)

    # Extract the operands and operator from the request
    a = request['a']
    b = request['b']
    op = request['op']
    expression = request['expression']

    logging.debug('Received request: a=%s, b=%s, op=%s, expression=%s',
                  a, b, op, expression)

    # Evaluate the expression and send the response
    if op == '+':
        result = a + b
    elif op == '-':
        result = a - b
    elif op == '*':
        result = a * b
    elif op == '/':
        result = a / b

    response = {'result': result, 'expression': expression}
    response_data = json.dumps(response).encode()

    writer.write(response_data)
    await writer.drain()
    writer.close()

    logging.debug('Sent response: result=%s, expression=%s', result, expression)

async def main():
    server = await asyncio.start_server(handle_client, '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
