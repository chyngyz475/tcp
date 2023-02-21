import asyncio
import json
import logging

logging.basicConfig(filename='client.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s: %(message)s')

async def make_request(expression):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)




    a, op, b = expression.split()

    request = {'a': int(a), 'b': int(b), 'op': op, 'expression': expression}
    request_data = json.dumps(request).encode()

    writer.write(request_data)
    await writer.drain()

    response_data = await reader.read()
    response = json.loads(response_data)

    writer.close()

    logging.debug('Received response: result=%s, expression=%s',
                  response['result'], response['expression'])

    return response['result']

async def main():
    expression = input('Enter a mathematical expression: ')
    result = await make_request(expression)
    print(f'Result: {result}')

if __name__ == '__main__':
    asyncio.run(main())