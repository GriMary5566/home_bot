import tiktoken

string = 'You are a helpful assistant.'
role = 'system'
encoding = tiktoken.encoding_for_model('gpt-3.5-turbo')
string_tokens = len(encoding.encode(string))
role_tokens =  len(encoding.encode(role))
num_tokens = 4 + string_tokens + role_tokens
print(string_tokens)
print(role_tokens)
print(num_tokens)