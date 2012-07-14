from correlation import pearson_similarity
import memcache
mc = memcache.Client(['127.0.0.1:11211'], debug=0)
mc.add("keys", [])

your_ratings = {}

def movie_data():
	moviedb_dict = {}
	f = open('u.item')
	movie_genres = []
	for line in f.readlines():
		movie_info = line.split('|')
		movie = {}
		key = movie_info[0]
		movie["id"] = movie_info[0]
		movie["title"] = movie_info[1]
		movie["release date"] = movie_info[2]
		movie["video release date"] = movie_info[3]
		movie["IMDB URL"] = movie_info[4]
		movie["genre_ids"] = movie_info[5:]	
		moviedb_dict[key] = movie
	f.close()
	return moviedb_dict

def genre():
	genre_dict = {}
	f = open('u.genre')
	for line in f.readlines():
		stripped_line = line.strip()
		if len(stripped_line) == 0:
			continue
		genre = stripped_line.split("|")
		key = int(genre[1])
		genre_dict[key] = genre[0]
	for movie_id, movie in MOVIES.items():
		genres = []
		for i in range(len(movie['genre_ids'])):
			if int(movie['genre_ids'][i]) == 1:
				genres.append(genre_dict[i])
		movie["genre(s)"] = ", ".join(genres)
	f.close()

def movie_details(movie_id):
	movie = MOVIES[movie_id]
	title = movie["title"]
	genre = movie["genre(s)"]
	return "Movie number %s: %s, is categorized as %s " % (movie["id"], title, genre)

def ratings_data():
	ratingsdb_dict = {}
	f = open("u.data")
	for line in f.readlines():
		stripped_line = line.strip()
		data = stripped_line.split()
		user_id = data[0]
		movie_id = data[1]
		rating = int(data[2])
		if ratingsdb_dict.get(movie_id) is None:
			ratingsdb_dict[movie_id] = {user_id: rating}
		else:
			ratingsdb_dict[movie_id][user_id] = rating
	return ratingsdb_dict

def get_avg_movie_rating(movie_id):
	"""add all of the ratings for a movie and divide by number of ratings"""
	#ratingsdb = ratings_data()
	movie_id_dict = RATINGS[movie_id]
	ratings = movie_id_dict.values()
	length = len(ratings)
	addition = sum(ratings)
	average_rating = float(addition)/length
	average = round(average_rating, 1)
	return "The average rating of %s is %d" % (movie_id, average)

def get_user_rating(movie_id, user_id):
	#ratingsdb = ratings_data()
	movie_id_dict = RATINGS[movie_id]
	if movie_id_dict.get(user_id) == None:
		print "This user has not rated this movie. Epic Fail!!!"
	else:	
		rating = movie_id_dict[user_id]
		print "user %s rated movie id %s at a %d" % (user_id, movie_id, rating)

def user_data():
	userdb = {}
	f = open("u.user")
	for user in f.readlines():
		user_info = user.split("|")
		user = {}
		key = user_info[0]
		user["id"] = user_info[0]
		user["age"] = user_info[1]
		user["gender"] = user_info[2]
		user["occupation"] = user_info[3]
		user["zip code"] = user_info[4]
		userdb[key] = user
	f.close()
	return userdb

def get_user(user_id):
	user = USERS[user_id]
	gender = user["gender"]
	occupation = user["occupation"]
	age = user["age"]
	return "User number %s: is a %s %s, age %s" % (user["id"], gender, occupation, age)

def give_a_rating(movie_id, rating):
	your_ratings[movie_id] = rating
	mc.set(movie_id, rating)
	keys_list = mc.get("keys")
	keys_list.append(movie_id)
	mc.set("keys", keys_list)
	# "You rated movie: %s at %s stars" % (movie_id, rating)

def prediction(movie_id):
	similarities =[]
	keys_list = mc.get("keys")
	for key in keys_list:
		sim = pearson_similarity(RATINGS, key, movie_id)
		similarities.append((sim, key))
	similarities.sort()
	best_guess_tup = similarities[-1]
	bg_sim = best_guess_tup[0]
	bg_movie = best_guess_tup[1]
	rating = mc.get(bg_movie)
	
	return "Our best guess for movie %s: is %s stars" % (movie_id, rating)

def main():
	global MOVIES 
	global USERS
	global RATINGS
	global YOUR_RATING
	MOVIES = movie_data()
	USERS = user_data()
	RATINGS = ratings_data()
	print prediction("45")
	genre()
	print movie_details("45")
	print get_user("4")
	get_user_rating("4", "4")
	give_a_rating("5", "4")
	print movie_details("350")
	

if __name__ == '__main__':
	main()