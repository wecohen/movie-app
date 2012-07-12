def movie_data():
	genre = ['unknown', 'Action', 'Adventure', 'Animation', 'Children\'s', 'Comedy',
				'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror', 'Musical',
				'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
	moviedb_dict = {}
	f = open('u.item')
	for line in f.readlines():
		movie_info = line.split('|')
		movie = {}

		key = movie_info[0]
		# sub_list = movie_info[1:]
		# moviedb_dict[key] = sub_list
		movie["id"] = movie_info[0]
		movie["title"] = movie_info[1]
		movie["release date"] = movie_info[2]
		movie["video release date"] = movie_info[3]
		movie["IMDB URL"] = movie_info[4]
		movie_genres = []
		movie["genre(s)"] = movie_genres
		genre_ids = movie_info[5:]
		for i in range(len(genre_ids)):
			if genre_ids[i] == 1:
				movie_genre.append(genre[i])
		moviedb_dict[key] = movie

	f.close()
	return moviedb_dict

def movie_details(movie_id):
	movie_db = movie_data()
	movie = movie_db[movie_id]
	print movie
	title = movie["title"]
	genre = movie["genre(s)"]
	return "%s: %s, is categorized as %s " % (movie["id"], title, genre)

def user_data():
	userdb = {}
	user = {}
	f = open("u.user")
	for user in f.readlines():
		user_info = user.split("|")
		userdb[user_info[0]] = user_info[1:]
		user["age"] = user_info[1]
		user["gender"] = user_info[2]
		user["occupation"] = user_info[3]
		user["zip code"] = user_info[4]
	f.close()
	return userdb

def get_user(user_id):
	user_db = user_data()
	user = user_db[user_id]
	gender = user["gender"]
	occupation = user["occupation"]
	age = user["age"]
	return "%d is a %s %s, age %d" % (user, gender, occupation, age)

def main():
	# movie_id = 42
	# user_id = 5
	print movie_details('42')
	# print get_user('5')

if __name__ == '__main__':
	main()