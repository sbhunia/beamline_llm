# import google.generativeai as genai

# genai.configure(api_key="YOUR_KEY")

# model = genai.GenerativeModel("gemini-1.5-flash")

# response = model.generate_content("Hello")

# print(response.text)

from google import genai

client = genai.Client(api_key="AIzaSyCTYNlYA6QUFIdIxO7y6sBfD70-2dXKut4")
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Hello"
)

print(response.text)

# from google import genai

# client = genai.Client(api_key="AIzaSyCTYNlYA6QUFIdIxO7y6sBfD70-2dXKut4")
# for m in client.models.list():
#     print(m.name)
