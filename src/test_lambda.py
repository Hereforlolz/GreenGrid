from lambda_function import lambda_handler

def test():
    event = {}  # Put your test event here if needed
    context = None  # Context can be None for simple tests
    
    response = lambda_handler(event, context)
    print("Lambda response:")
    print(response)

if __name__ == "__main__":
    test()
