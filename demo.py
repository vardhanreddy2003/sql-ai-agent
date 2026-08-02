import asyncio

async def fetch(delay,id):
    
    print("getching data:",id)
    await asyncio.sleep(delay)
    print("completed",id)
    return id
    
# async def main():
#     print("ok")
#     task1=fetch(1,2)
#     task2=fetch(2,1)
#     res1=await task1
#     res2=await task2
#     print(res1)
#     print(res2)

async def main():
    task1=asyncio.create_task(fetch(1,2))
    task2=asyncio.create_task(fetch(10,3))
    task3=asyncio.create_task(fetch(3,1))
    res1=await task1
    res2=await task2
    res3=await task3
    print(res1,res2,res3)
asyncio.run(main())