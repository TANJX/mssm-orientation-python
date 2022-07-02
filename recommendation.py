import csv

# TASK 1 - Separate Movie IDs and Movie names.
# TASK 2 - String Capitalization


def readAndFixInput():
    with open('input/RatingsInput.csv', newline='') as csvfile:
        output = []
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        # save the first line
        # UserID,UserName,UserAge,MovieID,MovieName,Rating
        output.append(",".join(next(spamreader)))
        for row in spamreader:
            # MovieName contains both MovieID and MovieName
            sp = row[4].split(",")
            row[3] = sp[0]
            # quote and capitalize the movie name
            row[4] = f'\"{sp[1].title()}\"'
            output.append(','.join(row))

        # save the fixed input to a new file
        f = open("output/Ratings.csv", "w")
        f.write("\n".join(output))
        f.close()

# TASK 3: Read new csv file


def readNewInput():
    csvfile = open('output/Ratings.csv', newline='')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    next(spamreader)  # skip the first line
    output = []
    # 0: UserID
    # 1: UserName
    # 2: UserAge
    # 3: MovieID
    # 4: MovieName
    # 5: Rating
    for row in spamreader:
        output.append({
            'id': row[0],
            'name': row[1],
            'age': int(row[2]),
            'movie_id': row[3],
            'movie_name': row[4],
            'rating': int(row[5])
        })
    return output


# TASK 4: Recommendation
def recommendByAge(ratings_dict, age, num):
    recommendation_score = []
    # calculate recommendation score for each movies
    for rating in ratings_dict:
        age_diff = abs(rating['age'] - age) + 1 # plus one to avoid divide by zero
        recommendation_score.append({
            'movie_id': rating['movie_id'],
            'movie_name': rating['movie_name'],
            'score': rating['rating'] / age_diff,
            'age': age,
            'age_diff': age_diff,
            'rating': rating['rating']
        })
    # sort the recommendation score
    recommendation_score.sort(key=lambda x: x['score'], reverse=True)
    # return the top num movie names
    return list(map(lambda x: x['movie_name'], recommendation_score[:num]))


def recommendNewUser(ratings_dict):
    csvfile = open('input/NewUsers.csv', newline='')
    spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    next(spamreader)  # skip the first line
    output = []
    # 0: UserName
    # 1: UserAge
    # 2: NoOfMoviesToRecommend
    # 3: Movies
    for row in spamreader:
        rec = recommendByAge(ratings_dict, int(row[1]), int(row[2]))
        row[3] = f'\"{",".join(rec)}\"'
        output.append(','.join(row))
    # save the fixed input to a new file
    f = open("output/Recommend.csv", "w")
    f.write("\n".join(output))
    f.close()


# main function
if __name__ == '__main__':
    readAndFixInput()
    ratings_dict = readNewInput()
    recommendNewUser(ratings_dict)
