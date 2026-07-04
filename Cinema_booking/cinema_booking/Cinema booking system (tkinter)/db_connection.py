from tkinter import messagebox as msb
from db_pool import DatabasePool
from utils import hash_password
from datetime import datetime,timedelta


class Connection():
    def __init__(self,host="127.0.0.1",user="root",password="root"):
        self.host=host
        self.user=user
        self.password=password
        self.database="cinema_booking"
        
        result=self._create_database_if_not_exists()
        if result[0]==0:
            msb.showerror("Failed",result[1])
            return
        DatabasePool.initialize(host=host,user=user,password=password,database=self.database)
        
        result=self._create_tables()
        if result[0]==0:
            msb.showerror("Failed",result[1])
            return
        
    def _create_database_if_not_exists(self):
        connection = DatabasePool.get_temp_connection(host=self.host,user=self.user,password=self.password)
        cursor = connection.cursor()
        try:
            # create database
            cursor.execute(f"CREATE SCHEMA IF NOT EXISTS `{self.database}` ;")
            return 1, f"Database '{self.database}' created or already exists."
        except Exception as e:
            return 0, f"Failed to create database: {e}"
        finally:
            connection.close()
    
    def _create_tables(self):
        table_queries=[
        "CREATE TABLE IF NOT EXISTS `users` (\
  `idusers` SMALLINT(4) UNSIGNED NOT NULL AUTO_INCREMENT,\
  `name` VARCHAR(100) NULL,\
  `surname` VARCHAR(250) NULL,\
  `username` VARCHAR(45) NOT NULL,\
  `password` VARCHAR(64) NOT NULL,\
  `access_level` TINYINT(1) UNSIGNED NOT NULL DEFAULT 2,\
  PRIMARY KEY (`idusers`),\
  UNIQUE INDEX `idusers_UNIQUE` (`idusers` ASC) VISIBLE,\
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE);",
        
        "CREATE TABLE IF NOT EXISTS  `movies` (\
  `idmovies` SMALLINT(4) UNSIGNED NOT NULL AUTO_INCREMENT,\
  `title` VARCHAR(150) NOT NULL,\
  `director` VARCHAR(250) NOT NULL,\
  `genre` VARCHAR(100) NOT NULL,\
  `duration` SMALLINT(3) UNSIGNED NOT NULL,\
  `release_date` DATETIME(1) NOT NULL,\
  `rating` DECIMAL(3,1) UNSIGNED NOT NULL,\
  PRIMARY KEY (`idmovies`),\
  UNIQUE INDEX `idmovies_UNIQUE` (`idmovies` ASC) VISIBLE,\
  UNIQUE INDEX `title_UNIQUE` (`title` ASC) VISIBLE);",
        
        "CREATE TABLE IF NOT EXISTS `halls` (\
  `idhalls` SMALLINT(4) UNSIGNED NOT NULL AUTO_INCREMENT,\
  `name` VARCHAR(100) NOT NULL,\
  `capacity` SMALLINT(3) UNSIGNED NOT NULL,\
  PRIMARY KEY (`idhalls`),\
  UNIQUE INDEX `idhalls_UNIQUE` (`idhalls` ASC) VISIBLE,\
  UNIQUE INDEX `name_UNIQUE` (`name` ASC) VISIBLE);",
        
        "CREATE TABLE IF NOT EXISTS `screening` (\
  `idscreens` SMALLINT(4) UNSIGNED NOT NULL AUTO_INCREMENT,\
  `movie` SMALLINT(4) UNSIGNED NOT NULL,\
  `hall` SMALLINT(4) UNSIGNED NOT NULL,\
  `screening_datetime` DATETIME(2) NOT NULL,\
  `ticket_price` DECIMAL(4,1) UNSIGNED NOT NULL,\
  PRIMARY KEY (`idscreens`),\
  UNIQUE INDEX `idscreens_UNIQUE` (`idscreens` ASC) VISIBLE,\
  INDEX `movie_idx` (`movie` ASC) VISIBLE,\
  INDEX `hall_idx` (`hall` ASC) VISIBLE,\
  CONSTRAINT `movie`\
    FOREIGN KEY (`movie`)\
    REFERENCES `movies` (`idmovies`)\
    ON DELETE RESTRICT\
    ON UPDATE RESTRICT,\
  CONSTRAINT `hall`\
    FOREIGN KEY (`hall`)\
    REFERENCES `halls` (`idhalls`)\
    ON DELETE RESTRICT\
    ON UPDATE RESTRICT);",
        
        "CREATE TABLE IF NOT EXISTS `reservations` (\
  `idreservations` INT UNSIGNED NOT NULL AUTO_INCREMENT,\
  `user` SMALLINT(4) UNSIGNED NOT NULL,\
  `screening` SMALLINT(4) UNSIGNED NOT NULL,\
  `seats_count` TINYINT(2) UNSIGNED NOT NULL,\
  `reserved_at` DATETIME(2) NOT NULL,\
  PRIMARY KEY (`idreservations`),\
  UNIQUE INDEX `idreservations_UNIQUE` (`idreservations` ASC) VISIBLE,\
  INDEX `user_idx` (`user` ASC) VISIBLE,\
  INDEX `screening_idx` (`screening` ASC) VISIBLE,\
  CONSTRAINT `user`\
    FOREIGN KEY (`user`)\
    REFERENCES `users` (`idusers`)\
    ON DELETE RESTRICT\
    ON UPDATE RESTRICT,\
  CONSTRAINT `screening`\
    FOREIGN KEY (`screening`)\
    REFERENCES `screening` (`idscreens`)\
    ON DELETE RESTRICT\
    ON UPDATE RESTRICT);"
]
        try:
            with DatabasePool.get_cursor() as cursor:
                for query in table_queries:
                    cursor.execute(query)
            return 1, "All tables created successfully."
        except Exception as e:
            return 0, f"Failed to create tables: {e}"
    
    def check_connection(self):
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute("SELECT 1")
            return True
        except:
            return False
  
    def insert_user(self,name,surname,username,password):    
        hashed_password=hash_password(password,username)
        query="INSERT INTO `users` (`name`, `surname`, `username`, `password`) VALUES (%s, %s, %s, %s);"
        values=(name,surname,username,hashed_password)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query, values)
            return 1, "User created successfully!"
        except Exception as e:
            return 0, f"Create user failed: {e}"
                
    def login(self, username, password):
        query = "SELECT idusers, username, password, access_level FROM `users` where username = %s;"
        value = (username,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query, value)
                item = cursor.fetchone()
            
            if item is None:
                return -1, "User doesn't exist!"
            if hash_password(password, username) == item[2]:
                return 1, "Login done successfully!", item[3], item[0]
            else:
                return 0, "Wrong password!"
        except Exception as e:
            return -2, f"Database error: {e}"
    
    def search_reservation(self,user_id,access_level,reservation_id,username,screen_id,seat_count,reserved_at,ticket_price,screening_datetime,hall,movie,director,duration,rating):
        query="SELECT idreservations,username,screening,seats_count,reserved_at,ticket_price,screening_datetime,`halls`.name,title,director,duration,rating FROM `reservations` join `users` on user=idusers join `screening` on screening=idscreens join `halls` on  hall=idhalls join `movies` on movie=idmovies  where 1=1"    
        values=[]
        if reservation_id!="":
            query+=" and idreservations=%s"
            values.append(f"{reservation_id}")
        if username!="":
            query+=" and username like %s"
            values.append(f"%{username}%")
        if screen_id!="":
            query+="  and screening=%s"
            values.append(f"{screen_id}")
        if seat_count!="":
            query+=" and seats_count=%s"
            values.append(f"{seat_count}")
        if reserved_at!="":
            query+=" and reserved_at>=%s"
            values.append(f"{reserved_at}")
        if ticket_price!="":
            query+=" and ticket_price>=%s"
            values.append(f"{ticket_price}")
        if screening_datetime!="":
            query+=" and screening_datetime>=%s"
            values.append(f"{screening_datetime}")
        if hall!="":
            query+=" and `halls`.name like %s"
            values.append(f"%{hall}%")
        if movie!="":
            query+=" and title like %s"
            values.append(f"%{movie}%")
        if director!="":
            query+=" and director like %s"
            values.append(f"%{director}%")
        if duration!="":
            query+=" and duration>=%s"
            values.append(f"{duration}")
        if rating!="":
            query+=" and rating>=%s"
            values.append(f"{rating}")
        if access_level==1:
            query+=" order by reserved_at;"
        else:
            if username=="":user_id_=user_id
            else:
                temp=self.get_user_id(username)
                if temp[0]==1:
                    user_id_=temp[1]
                else:
                    return -1,temp[1]
            query+=" and `idusers`=%s order by reserved_at;"
            values.append(f"{user_id_}")
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
                items=cursor.fetchall()
                return 1,items
        except Exception as e:
            return 0,f"Failed to search reservation : {e}"
    
    def add_reservation(self,user_id,screen_id,seat_count,reserved_at):
        query="INSERT INTO `reservations` (`user`, `screening`, `seats_count`, `reserved_at`) VALUES (%s, %s, %s, %s);"
        values=(user_id,screen_id,seat_count,reserved_at)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
            return 1,"Screen reserved successfully!"
        except Exception as e:
            return 0,f"Reservation doesn't submit.\n\n {e}"
    
    def get_reservation_data(self,reservation_id):
        query="SELECT username,screening,seats_count FROM reservations join users on reservations.user=idusers WHERE (idreservations=%s);"
        value=(reservation_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
                if item is None:
                    return 0,"Reservation doesn't exist."
            return 1,item 
        except Exception as e:
            return -2,f"Database error:  {e}"    
    
    def update_reservation(self,reservation_id,user_id_,screen_id,seat_count,reserved_at):
        query="UPDATE `reservations` SET\
            `user` = %s, `screening` = %s, `seats_count` = %s, `reserved_at` = %s \
            WHERE (`idreservations` = %s);" 
        values=(user_id_,screen_id,seat_count,reserved_at,reservation_id)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
            return 1,f"Updating reservation '{reservation_id}' has been done successfully!"  
        except Exception as e:
            return 0,f"Updating reservation failed :\n\n{e}"  
        
    def delete_reservation(self,reservation_id,screen_id):
        check_query="SELECT * FROM `reservations` where (`idreservations`=%s) and (`screening`=%s);"
        check_values=(reservation_id,screen_id)
        try:
            with DatabasePool.get_cursor() as cursor:    
                cursor.execute(check_query,check_values)
                item=cursor.fetchone()
                if item is None:
                    return -1,"This reservation doesn't exist!"
        
            delete_query="DELETE FROM `reservations` WHERE (`idreservations` = %s) and (`screening`=%s);"
            with DatabasePool.get_cursor() as cursor: 
                cursor.execute(delete_query,check_values)
                return 1,f"Reservation {reservation_id} deleted successfully!"
        except Exception as e:
            return 0, f"Cannot delete reservation '{reservation_id}' : {e}"
                   
    def insert_movie(self,title,director,genre,duration,release_date,rating,movie_id=None):
        query="INSERT INTO `movies` (`idmovies`,`title`, `director`, `genre`, `duration`, `release_date`, `rating`) VALUES (%s ,%s, %s, %s, %s, %s, %s);"  
        values=movie_id,title,director,genre,duration,release_date,rating
        
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query, values)
            return 1, "Movie added successfully!"
        except Exception as e:
            return 0, f"Fail to add movie: {e}"
         
    def get_movie_data(self,movie_id):
        query="SELECT * FROM `movies` where (idmovies=%s);"
        value=movie_id
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0,"Movie doesn't exist."
            return 1,item 
        except Exception as e:
            return -1, f"Database error: {e}"
        
    def update_movie(self,movie_id,title,director,genre,duration,release_date,rating):        
        query="UPDATE `movies` SET\
            `title` = %s, `director` = %s, `genre` = %s, `duration` = %s, `release_date` = %s, `rating` = %s\
            WHERE (`idmovies` =%s);" 
        values=title,director,genre,duration,release_date,rating,movie_id
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
            return 1,f"Updating movie '{movie_id}' has been done successfully!"  
        except Exception as e:
            return 0,f"Updating movie failed:\n\n{e}"

    def delete_movie(self,movie_id,title):
        check_query="SELECT * FROM `movies` WHERE (`idmovies` = %s) and (`title` = %s);"
        check_values=(movie_id,title)
        try:
            with DatabasePool.get_cursor() as cursor:    
                cursor.execute(check_query,check_values)
                item=cursor.fetchone()
                if item is None:
                    return -1,"Movie doesn't exist!"
        
            delete_query="DELETE FROM `movies` WHERE (`idmovies` = %s) and (`title` = %s);"
            with DatabasePool.get_cursor() as cursor:   
                cursor.execute(delete_query,check_values)
                return 1,f"Movie '{title}' deleted successfully!"
        except Exception as e:
            return 0, f"Cannot delete movie.\n\n{e}"

    def search_movie(self,movie_id,title,director,genre,duration,release_date,rating):
        query="SELECT * FROM movies where 1=1"
        values=[]
        if movie_id!="":
            query+=" and idmovies=%s"
            values.append(f"{movie_id}")
        if title!="":
            query+=" and title like %s"
            values.append(f"%{title}%")
        if director!="":
            query+=" and director like %s"
            values.append(f"%{director}%")
        if genre!="":
            query+=" and genre like %s"
            values.append(f"%{genre}%")
        if duration!="":
            query+=" and duration>=%s"
            values.append(duration)
        if release_date!="":
            query+=" and release_date>=%s"
            values.append(release_date)
        if rating!="":
            query+=" and rating>=%s"
            values.append(rating)
        query+=";"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query, values)  
                items = cursor.fetchall()
                return 1, items
        except Exception as e:
                return 0, f"Failed to search movie: {e}"
    
    def add_hall(self,name,capacity):
        query="INSERT INTO `halls` (`name`, `capacity`) VALUES (%s, %s);"
        values=(name,capacity)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
                return 1,f"Hall '{name}' added successfully!"
        except Exception as e:
            return 0,f"Hall '{name}' already exists!: {e}"
    
    def delete_hall(self,name):
        check_query="SELECT * FROM `halls` where name=%s;"
        check_value=(name,)
        with DatabasePool.get_cursor() as cursor:
            cursor.execute(check_query,check_value)
            item=cursor.fetchone()
            if item is None:
                return -1,f"Hall '{name}' doesn't exist!"
        try:
            with DatabasePool.get_cursor() as cursor:       
                delete_query="DELETE FROM `halls` WHERE (`name` = %s);"
                cursor.execute(delete_query,check_value)
                return 1,"Hall deleted successfully!"
        except Exception as e:
            return 0, f"Cannot delete '{name}'\n\n{e}" 
    
    def reserve_ticket(self,screen_id):
        query="SELECT idscreens,screening_datetime,name,ticket_price,title,director,duration,genre,release_date,rating FROM `screening` join `movies` join `halls` where movie=idmovies and hall=idhalls and idscreens=%s; "
        value=(screen_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
                return 1,item
        except Exception as e:
            return 0,f"An error occurred: \n\n {e}" 
        
    def check_and_reserve(self,user_id,seat_count,screen_id):
        query="SELECT COALESCE(SUM(r.seats_count), 0) AS total_reserved,h.capacity FROM screening s JOIN halls h ON s.hall = h.idhalls LEFT JOIN reservations r ON r.screening = s.idscreens WHERE s.idscreens = %s;"
        value=(screen_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
                total_reserved=item[0]
                capacity=item[1]
            
            if total_reserved==capacity:
                return -1,"Sorry,Screen capacity already completed!"
            elif seat_count+total_reserved<=capacity:
                reserved_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                result=self.add_reservation(user_id,screen_id,seat_count,reserved_at)
                return result
            elif seat_count+total_reserved>capacity:
                return 0,"Seats count you entered is more than screen capacity.\nTry again later or reduce seats count."
        except Exception as e:
            return -2, f"Database error in check_and_reserve: {e}"
    
    def search_screen(self,screen_id,access_level,movie,hall,screening_datetime,ticket_price):
        if access_level==1:
            query="SELECT idscreens,screening_datetime,ticket_price,title,director,duration,name FROM `screening` join `movies` join `halls` where movie=idmovies and hall=idhalls"   
        else:
            query="SELECT idscreens,screening_datetime,ticket_price,title,director,duration,name FROM `screening` join `movies` join `halls` where movie=idmovies and hall=idhalls and screening_datetime>now()" 
        
        values=[]
        if screen_id!="":
            query+=" and idscreens=%s"
            values.append(f"{screen_id}")
        if movie!="":
            query+=" and title like %s"
            values.append(f"%{movie}%")
        if hall!="":
            query+=" and name = %s"
            values.append(f"{hall}")
        if screening_datetime!="":
            query+=" and screening_datetime >= %s"
            values.append(f"{screening_datetime}")
        if ticket_price!="":
            query+=" and ticket_price >= %s"
            values.append(ticket_price)
        query += " ORDER BY screening_datetime;"
        
        try:
            with DatabasePool.get_cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                items = cursor.fetchall()
            return 1, items
        except Exception as e:
            return 0, f"Failed to search screens: {e}"
    
    def add_screen(self,movie,hall,screening_datetime,ticket_price,screen_id=None):
        result_hall_id=self.get_hall_id(hall)
        if result_hall_id[0]==1:
            hall_id=result_hall_id[1]
        else: return 0, f"Error: {result_hall_id[1]}"
        
        result_movie_id=self.get_movie_id(movie)
        if result_movie_id[0]==1:
            movie_id=result_movie_id[1]
        else:  return 0, f"Error {result_movie_id[1]}"
        
        query="INSERT INTO `screening` (`idscreens`,`movie`, `hall`, `screening_datetime`, `ticket_price`) VALUES (%s ,%s, %s, %s, %s);"
        values=(screen_id,movie_id,hall_id,screening_datetime,ticket_price)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
            return 1, "New screen added to database successfully!"
        except Exception as e:
            return 0, f"Failed to add new screen: \n\n{e}"
    
    def get_screen_data(self,screen_id):
        query="SELECT idscreens,title,`halls`.name,screening_datetime,ticket_price\
            FROM `screening` join `movies` on movie=idmovies join `halls` on hall=idhalls\
             where (idscreens=%s);"
        value=(screen_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0,"Screen doesn't exist."
            else: return 1,item  
        except Exception as e:
            return -2, f"Database error: {e}" 
   
    def update_screen(self,screen_id,movie,hall,screening_datetime,ticket_price):
        query="UPDATE `screening` SET `movie` = %s, `hall` = %s, `screening_datetime` = %s, `ticket_price` = %s\
            WHERE (`idscreens` = %s);"       
        result_hall_id=self.get_hall_id(hall)
        if result_hall_id[0]==1:
            hall_id=result_hall_id[1]
        else: return 0, f"Error: {result_hall_id[1]}"
        
        result_movie_id=self.get_movie_id(movie)
        if result_movie_id[0]==1:
            movie_id=result_movie_id[1]
        else:  return 0, f"Error: {result_movie_id[1]}"
        
        values=(movie_id,hall_id,screening_datetime,ticket_price,screen_id)
        
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
                return 1,f"Updating screen '{screen_id}' has been done successfully!"  
        except Exception as e:
            return 0,f"Updating screen failed :\n\n{e}"
           
    def delete_screen(self,screen_id,movie):
        check_query="SELECT * FROM `screening` where (`idscreens`=%s) and (`movie`=%s);"
        result_movie_id=self.get_movie_id(movie)
        if result_movie_id[0]==1:
            movie_id=result_movie_id[1]
        else:  return 0, f"Error: {result_movie_id[1]}"
        
        check_values=(screen_id,movie_id)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(check_query,check_values)
                item=cursor.fetchone()
            if item is None:
                return -1,"Screen doesn't exist!"
            delete_query="DELETE FROM `screening` WHERE (`idscreens` = %s) and (`movie`=%s);"
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(delete_query,check_values)
                return 1,f"Screen {screen_id} deleted successfully!"
        except Exception as e:
            return 0, f"Cannot delete screen: {e}"

    def search_user(self,user_id,name,surname,username,access_level):
        query="SELECT idusers,name,surname,username,access_level FROM users where 1=1"
        values=[]
        if user_id!="":
            query+=" and idusers=%s"
            values.append(f"{user_id}")
        if name!="":
            query+=" and name like %s"
            values.append(f"%{name}%")
        if surname!="":
            query+=" and surname like %s"
            values.append(f"%{surname}%")
        if username!="":
            query+=" and username like %s"
            values.append(f"%{username}%")
        if access_level!="":
            query+=" and access_level=%s"
            values.append(access_level)
        query += " ORDER BY idusers;"
        
        try:
            with DatabasePool.get_cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                items = cursor.fetchall()
            return 1, items
        except Exception as e:
            return 0, f"Failed to search users: {e}"
    
    def get_user_data(self,user_id):
        query="SELECT idusers,`users`.name,surname,username,access_level FROM `users` where (idusers=%s);"
        value=(user_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0,"User doesn't exist."
            return 1,item 
        except Exception as e:
            return -2,f"Database error: {e}" 
    
    def update_user(self,user_id,name,surname,username,access_level):
        query="UPDATE `users` SET `name` = %s, `surname` = %s, `username` = %s, `access_level` = %s\
            WHERE (`idusers` = %s);"       
        values=(name,surname,username,access_level,user_id)
        
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
                return 1,f"Updating user '{user_id}' has been done successfully!"  
        except Exception as e:
            return 0,f"Updating user failed:\n\n{e}" 
    
    def delete_user(self,user_id,username):
        check_query="SELECT * FROM `users` where (`idusers`=%s) and (`username`=%s);"
        check_values=(user_id,username)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(check_query,check_values)
                item=cursor.fetchone()
            if item is None:
                return -1,"User doesn't exist!"
            delete_query="DELETE FROM `users` WHERE (`idusers`=%s) and (`username`=%s);"
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(delete_query,check_values)
            return 1,f"User {username} deleted successfully!"
        except Exception as e:
            return 0, f"Cannot delete user '{username}'\n\n{e}"
        
    def edit_profile(self,user_id,access_level,name,surname,username,password,new_access_level):
        hashed_password=hash_password(password,username)
        if access_level==1:
            if new_access_level not in ["1","2"]:
                return 0 ,"Access level can't be empty!"
   
            query="UPDATE `users` SET `name` = %s, `surname` = %s, `username` = %s, `password` = %s, `access_level` = %s\
                WHERE (`idusers` = %s);"
            values=(name,surname,username,hashed_password,new_access_level,user_id)               
        else:
            query="UPDATE `users` SET `name` = %s, `surname` = %s, `username` = %s, `password` = %s\
                WHERE (`idusers` = %s);"
            values=(name,surname,username,hashed_password,user_id)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,values)
            return 1, "Profile updated successfully!"
        except Exception as e:
            return 0, f"Update profile failed: {e}"


#### Helper methods

    
    def set_combo_reservation_id_view_reservation_window_values(self,user_id,access_level):
        if access_level==1:
            query="SELECT idreservations FROM `reservations`;"
            try:
                with DatabasePool.get_cursor() as cursor:
                    cursor.execute(query)
                    return cursor.fetchall()
            except:
                return []    
        else:
            query="SELECT idreservations FROM `reservations` where (`user`=%s);"
            value=(user_id,)
            try:
                with DatabasePool.get_cursor() as cursor:
                    cursor.execute(query,value)
                    return cursor.fetchall()
            except:
                return []
          
    def set_combo_hall_screen_window_values(self):
        query="SELECT name FROM `halls`;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 
    
    def set_combo_movie_screen_window_values(self):
        query="SELECT title FROM `movies`;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 
    
    def set_combo_screen_id_screen_window_values(self,access_level):
        if access_level==1:
            query="SELECT idscreens FROM `screening`;"
        else:
            query="SELECT idscreens FROM `screening` where screening_datetime>now() ;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 
    
    def set_combo_movie_id_movie_window_values(self):
        query="SELECT idmovies FROM `movies`;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 

    def set_combo_list_hall_window_values(self):
        query="SELECT name,capacity FROM `halls`;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 
        
    def set_combo_user_id_users_window_values(self):
        query="SELECT idusers,username FROM `users`;"
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        except Exception as e:
            return [] 
       
    def get_user_id(self,username):
        query="SELECT idusers,username FROM `users` where username=%s;"
        value=(username,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0, f"Username '{username}' not exists!"
            else: return 1,item[0]
        except Exception as e:
            return -1,f"Database error: {e}"                  
    
    def get_movie_id(self,movie):
        query="SELECT idmovies,title FROM `movies` where title=%s;"
        value=(movie,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0, f"Movie '{movie}' not exists!"
            else: return 1,item[0]
        except Exception as e:
            return -1, f"Database error: {e} "
        
    def get_hall_id(self,hall):
        query="SELECT idhalls,name FROM `halls` where name=%s;"
        value=(hall,)
        try:
            with DatabasePool.get_cursor() as cursor:    
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0, f"Hall '{hall}' not exists!"
            else: return 1,item[0]
        except Exception as e:
            return -1,f"Database error: {e}"   
         
    def get_screening_datetime(self,screen_id):
        query="SELECT idscreens,screening_datetime FROM `screening` where idscreens=%s;"
        value=(screen_id,)
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query,value)
                item=cursor.fetchone()
            if item is None:
                return 0,"Screen doesn't exist."    
            return 1,item[1]
        except Exception as e:
            return -1 , f"Database error: {e}"
            
    def is_hall_free(self,hall,screening_datetime,movie,exclude_screen_id=None):
        result_hall_id=self.get_hall_id(hall)
        if result_hall_id[0]==1:
            hall_id=result_hall_id[1]
        else: return False
        
        result_movie_id=self.get_movie_id(movie)
        if result_movie_id[0]==1:
            movie_id=result_movie_id[1]
        else: return False
        
        result_duration=self.get_movie_data(movie_id)
        if result_duration[0]==1:
            duration=result_duration[1][4]
        else: return False
        
        dt_screening_datetime   =datetime.strptime(screening_datetime,'%Y-%m-%d %H:%M:%S')
        dt_end_datetime         =dt_screening_datetime+timedelta(minutes=duration)
        end_datetime            =datetime.strftime(dt_end_datetime,'%Y-%m-%d %H:%M:%S')
        
        query = "SELECT COUNT(*) FROM screening s JOIN movies m ON s.movie = m.idmovies WHERE s.hall = %s\
            AND s.screening_datetime < %s AND DATE_ADD(s.screening_datetime, INTERVAL m.duration MINUTE) > %s"
        values = [hall_id, end_datetime, screening_datetime]
        
        # delete current screen from checking when update screen.
        if exclude_screen_id is not None:
            query += " AND s.idscreens != %s"
            values.append(exclude_screen_id)
        
        try:
            with DatabasePool.get_cursor() as cursor:
                cursor.execute(query, values)
                result = cursor.fetchone()
            # if (result[0] == 0)--> TRUE ==> free hall
            return result[0] == 0
        except Exception as e:
            return False
    
    
        
    







    
        
