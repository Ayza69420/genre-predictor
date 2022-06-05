import pandas as pd

t_d, d = [], []
classifying = {"male": {}, "female": {}}

train_data_path = "./train_data.csv"
test_data_path = "./test_data.csv"

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

for row in train_data.iterrows():
    age, gender, genre= row[1].values
    
    t_d.append([age, gender, genre])

for row in test_data.iterrows():
    age, gender = row[1].values

    d.append([age, gender])

for i in t_d:
    _, gender, genre = i
    gender = gender.lower()

    if genre not in classifying[gender]:
        ages = [k_age for k_age, k_gender, k_genre in t_d if k_gender.lower() == gender and k_genre == genre]

        classifying[gender][genre] = range(min(ages),max(ages)+1)

for i in d:
    age, gender = i
    gender = gender.lower()
    possibilities = [genre for genre in classifying[gender]if age in classifying[gender][genre]]

    for k in possibilities[1:]:
        min_a, min_b = classifying[gender][possibilities[0]][0], classifying[gender][k][0]
        differences = [age-min_a, age-min_b]

        if differences[0] != differences[1]:
            possibilities.remove([possibilities[0],k][max(differences)==age-min_b])
        else: 
            occurrences_a = sum([1 for _, k_gender, k_genre in t_d if k_gender == gender and k_genre == possibilities[0]])
            occurrences_b = sum([1 for _, k_gender, k_genre in t_d if k_gender == gender and k_genre == k])
            
            possibilities.remove([possibilities[0],k][min(occurrences_a, occurrences_b)==occurrences_b])
    
    print(f"{age} {gender} : {'/'.join(possibilities)}" if possibilities else None)


input("\n> Exit")
