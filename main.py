import pandas as pd

t_d, d = [], []

classifying = {"male": {}, "female": {}}
occurrences = {"male": {}, "female": {}}
genres = set()

train_data_path = "./train_data.csv"
test_data_path = "./test_data.csv"

train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

for row in train_data.iterrows():
    age, gender, genre= row[1].values
    
    t_d.append([age, gender.lower(), genre])
    occurrences[gender.lower()][genre] = occurrences.get(genre, 0)+1
    genres.add(genre)

for row in test_data.iterrows():
    age, gender = row[1].values

    d.append([age, gender.lower()])

for genre in genres:
    for gender in ["male", "female"]:
        ages = [k_age for k_age, k_gender, k_genre in t_d if k_gender == gender and k_genre == genre]
        
        if ages:
            classifying[gender][genre] = range(min(ages),max(ages)+1)

for i in d:
    age, gender = i
    possibilities = [genre for genre in classifying[gender]if age in classifying[gender][genre]]

    for k in possibilities[1:]: # comparing each possibility with the first possibility following the below rules
        min_a, min_b, max_a, max_b = classifying[gender][possibilities[0]].start, classifying[gender][k].start, classifying[gender][possibilities[0]].stop, classifying[gender][k].stop
        differences = [abs(age-min_a), abs(age-min_b), abs(age-max_a), abs(age-max_b)]
        occ_a = occurrences[gender][possibilities[0]]
        occ_b = occurrences[gender][k]
        
        if differences[0] != differences[1]: # If the differences are not the same, look for the farthest one and remove it 
            possibilities.remove([possibilities[0],k][max(differences[0:2])==differences[1]])
        elif occ_a == occ_b and differences[-1] != differences[-2]: # otherwise, if the occurrences aren't equal, look for the least occurring genre and remove it
            possibilities.remove([possibilities[0],k][min(occ_a, occ_b)==occ_b])
        else: # if occurrences of a == occurrences of b look for the fathest one from the maximum and remove it, just like the minimum above
            possibilities.remove([possibilities[0],k][max(differences[3:5])==differences[3]])
                
    print(f"{age} {gender} : {'/'.join(possibilities)}" if possibilities else None)
