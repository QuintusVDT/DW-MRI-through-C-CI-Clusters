import os

path = "/globalscratch/users/d/u/dujardin/studies/study/data_1/"


for files in os.listdir(path):
  if ".bval" in files:
    fichier = os.path.join(path, files)
    with open(fichier, "r") as doc:
      content = doc.read()
      
    # Split the content by spaces to get a list of strings
    string_numbers = content.split()
    
    # Convert the list of strings to a list of numbers (int or float)
    numbers = [float(num) for num in string_numbers]
    print(files)
    print("total: ", len(numbers))
    print("0: ", numbers.count(0) + numbers.count(5))
    print("700: ", numbers.count(700) + numbers.count(695) + numbers.count(705))
    print("2000: ", numbers.count(1995) + numbers.count(2000) + numbers.count(2005))
    print("3000: ", numbers.count(3000) + numbers.count(2995) + numbers.count(3005))
    print("5000: ", numbers.count(5000) + numbers.count(4995) + numbers.count(5005))
    print("autre: ", len(numbers) - (numbers.count(0) + numbers.count(5) + numbers.count(700) + numbers.count(695) + numbers.count(705) + numbers.count(1995) + numbers.count(2000) + numbers.count(2005) + numbers.count(3000) + numbers.count(2995) + numbers.count(3005) + numbers.count(5000) + numbers.count(4995) + numbers.count(5005)))