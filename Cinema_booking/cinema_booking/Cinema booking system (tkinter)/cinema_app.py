from tkinter import *
from tkinter import messagebox as msb,ttk
from db_connection import Connection
from config import *
from utils import clear_entries
from datetime import datetime
from PIL import Image,ImageTk



try:
    connection = Connection()
    if not connection.check_connection():
        msb.showwarning("Couldn't connect", "Connecting to database failed!")
        exit()
except Exception as e:
    msb.showerror("Initialization Error", f"Failed to start application:\n\n{e}")
    exit()
    
lst_entry_screen_info_reserve_movie_window = []  # default
    
def change_window(hide_window:Tk,show_window:Tk):
    hide_window.withdraw()
    
    if hide_window==movie_window:
        temp=[combo_movie_id_movie_window,entry_title_movie_window,entry_director_movie_window,entry_genre_movie_window,entry_duration_movie_window,entry_release_date_movie_window,entry_rating_movie_window]
        clear_entries(temp)
        
    if hide_window==login_window:
        entry_password_login_window .delete(0,END)
    
    if hide_window==screen_window:
        temp=[combo_screen_id_screen_window,combo_movie_screen_window,combo_hall_screen_window,entry_screening_datetime_screen_window,entry_ticket_price_screen_window]
        clear_entries(temp)
        
    if hide_window==sign_up_window:
        temp=[entry_name_sign_up_window,entry_surname_sign_up_window,entry_username_sign_up_window,entry_password_sign_up_window,entry_password2_sign_up_window,entry_access_level_sign_up_window]
        clear_entries(temp)
        
    if show_window==sign_up_window:         setup_sign_up_window(hide_window)            
    if show_window==main_menu:              setup_main_menu()
    if show_window==view_reservation_window:setup_view_reservation_window()          
    if show_window==movie_window:           setup_movie_window()
    if show_window==screen_window:          setup_screen_window()                 
    if show_window==hall_window:            setup_hall_window()    
    if show_window==reserve_movie_window:   setup_reserve_movie_window()
    if show_window==users_window:           setup_users_window()
      
    show_window.deiconify()
        
def setup_sign_up_window(hide_window:Tk):
    if hide_window==root:
        sign_up_window                          .title("Sign up window")
        lbl_access_level_sign_up_window         .grid_forget()
        entry_access_level_sign_up_window       .grid_forget()
        btn_ok_sign_up_window                   .config(command=insert_user)
        btn_back_sign_up_window                 .config(command=lambda:change_window(sign_up_window,root)) 
    
    elif hide_window==users_window:
        sign_up_window                          .title("Add user window")
        lbl_access_level_sign_up_window         .grid(CNF_GRID_GENERAL,row=6,column=1)
        entry_access_level_sign_up_window       .grid(CNF_GRID_GENERAL,row=6,column=2)
        btn_ok_sign_up_window                   .config(command=insert_user)
        btn_back_sign_up_window                 .config(command=lambda:change_window(sign_up_window,users_window))
        
    elif hide_window==main_menu:
        sign_up_window                          .title("Profile window")
        btn_back_sign_up_window                 .config(command=lambda:change_window(sign_up_window,main_menu))
        btn_ok_sign_up_window                   .config(command=edit_profile)      
        if access_level==1:
            lbl_access_level_sign_up_window     .grid(CNF_GRID_GENERAL,row=6,column=1)
            entry_access_level_sign_up_window   .grid(CNF_GRID_GENERAL,row=6,column=2)
        else:
            lbl_access_level_sign_up_window     .grid_forget()
            entry_access_level_sign_up_window   .grid_forget()

        result=connection.get_user_data(user_id)
        if result[0]==1:
            result=result[1]
            entry_name_sign_up_window           .insert(0,result[1])
            entry_surname_sign_up_window        .insert(0,result[2])
            entry_username_sign_up_window       .insert(0,result[3])
            entry_access_level_sign_up_window   .insert(0,result[4])
        else:
            msb.showerror("Failed!",result[1])
            return
        
def setup_main_menu():
    global access_level
    if access_level==2:
        btn_manage_movies_main_menu         .grid_forget()
        btn_manage_halls_main_menu          .grid_forget()
        btn_manage_users_main_menu          .grid_forget()
        btn_view_reservation_main_menu      .config(text="View my reservations")
    else:
        btn_manage_movies_main_menu         .grid(CNF_GRID_GENERAL,row=2,column=1)
        btn_manage_halls_main_menu          .grid(CNF_GRID_GENERAL,row=3,column=1)
        btn_manage_users_main_menu          .grid(CNF_GRID_GENERAL,row=5,column=1)
        btn_view_reservation_main_menu      .config(text="View reservations")

def setup_view_reservation_window():
    global access_level
    search_reservation()
    result=connection.set_combo_reservation_id_view_reservation_window_values(user_id,access_level)
    result=sorted([item[0] for item in result])
    combo_reservation_id_view_reservation_window.config(values=[""]+result)

    if access_level==1:
        btn_add_view_reservation_window                 .grid(CNF_GRID_GENERAL,row=1,column=2)
        btn_update_view_reservation_window              .grid(CNF_GRID_GENERAL,row=1,column=3)
    else:
        btn_add_view_reservation_window                 .grid_forget()
        btn_update_view_reservation_window              .grid_forget()
        entry_username_view_reservation_window          .config(state="disabled")

def setup_movie_window():
    search_movie()
    result=connection.set_combo_movie_id_movie_window_values()
    result=[item[0] for item in result]
    combo_movie_id_movie_window.config(values=[""]+result)
    
def setup_screen_window():
    global access_level
    search_screen()
    result1=connection.set_combo_hall_screen_window_values()
    result2=connection.set_combo_movie_screen_window_values()
    result3=connection.set_combo_screen_id_screen_window_values(access_level)
    result1=[item[0] for item in result1]
    result2=[item[0] for item in result2]
    result3=[item[0] for item in result3]
    combo_hall_screen_window                .config(values=[""]+result1)
    combo_movie_screen_window               .config(values=[""]+result2)
    combo_screen_id_screen_window           .config(values=[""]+result3)
    
    if access_level==2:
        btn_add_screen_screen_window       .grid_forget()
        btn_update_screen_screen_window    .grid_forget()
        btn_delete_screen_screen_window    .grid_forget()
        btn_reserve_ticket_screen_window   .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=4,column=1)
    else:
        btn_reserve_ticket_screen_window   .grid_forget()
        btn_add_screen_screen_window       .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=2,column=1)
        btn_update_screen_screen_window    .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=3,column=1)
        btn_delete_screen_screen_window    .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=4,column=1)

def setup_hall_window():
    result5=connection.set_combo_list_hall_window_values()
    result5=[f"{item[0]} - ({item[1]})" for item in result5]  
    combo_list_hall_window.config(values=result5)
    
def setup_reserve_movie_window():
    for entry in lst_entry_screen_info_reserve_movie_window:
        entry.config(state="normal")
        entry.delete(0,END)
    entry_seat_count_reserve_movie_window.delete(0,END)

def setup_users_window():
    search_user()
    result1=connection.set_combo_user_id_users_window_values()
    result2=sorted([item[0] for item in list(result1)])
    combo_user_id_users_window.config(values=[""]+result2)
    result3=[item[1] for item in result1]
    combo_username_users_window.config(values=[""]+result3)

       
def insert_user():
    name=entry_name_sign_up_window          .get().strip()
    surname=entry_surname_sign_up_window    .get().strip()
    username=entry_username_sign_up_window  .get().strip()
    password=entry_password_sign_up_window  .get().strip()
    password2=entry_password2_sign_up_window.get().strip()
    
    if username=="":
        msb.showwarning("UsernameError","username can't be empty!")
        return
    
    if len(password)<5:
        msb.showwarning("PasswordError","password must be at least 5 characters!")
        return
    
    if password!=password2:
        msb.showwarning("PasswordError","passwords don't match!")
        return
    
    if name=="":    name=None
    if surname=="": surname=None
    
    result=connection.insert_user(name,surname,username,password)
    if result[0]==1:
        msb.showinfo("User created!",result[1])
        change_window(sign_up_window,root)
    else:
        msb.showerror("User not created!",result[1])
    
    temp=[entry_name_sign_up_window,entry_surname_sign_up_window,entry_username_sign_up_window,entry_password_sign_up_window,entry_password2_sign_up_window]
    clear_entries(temp)
    
    
def login():
    global access_level,user_id
    username=entry_username_login_window.get().strip()
    password=entry_password_login_window.get().strip()
    
    result=connection.login(username,password)
    if result[0]==-1:
        msb.showerror('UsernameError',result[1])
        entry_username_login_window.delete(0,END)
    
    elif result[0]==1:
        access_level=result[2]
        user_id=result[3]
        change_window(login_window,main_menu)
        
    elif result[0]==0:
        msb.showerror('PasswordError',result[1])
    
    elif result[0]==-2:
        msb.showerror('DatabaseError',result[1])
    
    entry_password_login_window.delete(0,END)


def search_reservation():
    global access_level,user_id
    reservation_id=combo_reservation_id_view_reservation_window         .get().strip()
    username=entry_username_view_reservation_window                     .get().strip()
    screen_id=entry_screen_id_view_reservation_window                   .get().strip()
    seat_count=entry_seat_count_view_reservation_window                 .get().strip()
    reserved_at=entry_reserved_at_view_reservation_window               .get().strip()
    ticket_price=entry_ticket_price_view_reservation_window             .get().strip()
    screening_datetime=entry_screening_datetime_view_reservation_window .get().strip()
    hall=entry_hall_view_reservation_window                             .get().strip()
    movie=entry_movie_view_reservation_window                           .get().strip()
    director=entry_director_view_reservation_window                     .get().strip()
    duration=entry_duration_view_reservation_window                     .get().strip()
    rating=entry_rating_view_reservation_window                         .get().strip()

    result=connection.search_reservation(user_id,access_level,reservation_id,username,screen_id,seat_count,reserved_at,ticket_price,screening_datetime,hall,movie,director,duration,rating)
    if result[0]==0 or result[0]==-1:
        msb.showerror("Failed!",result[1])
        return
    else:    
        result=result[1]
        treev_view_reservation_window.delete(*treev_view_reservation_window.get_children())
        for item in result:
            treev_view_reservation_window.insert("",END,values=item)


def add_reservation():
    username=entry_username_view_reservation_window                     .get().strip()
    screen_id=entry_screen_id_view_reservation_window                   .get().strip()
    reserved_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    temp=connection.get_user_id(username)
    try:
        seat_count=int(entry_seat_count_reserve_movie_window.get().strip()) 
    except:
        msb.showerror("Invalid seat count","Enter a valid number!")
        return
    if username=="" or screen_id=="" or seat_count=="":
        msb.showwarning("FormError","You should enter username,ID screen and seat counts correctly to submit a reservation.")
        return
    if temp[0] != 1:
        msb.showerror("Failed!", temp[1])
        return  
    
    user_id_=temp[1]
    if user_id_=="":
        msb.showerror("Not found!",f"User '{username}' doesn't exist!")
        return
    result=connection.add_reservation(user_id_,screen_id,int(seat_count),reserved_at)
    if result[0]==1:
        msb.showinfo("Done!",result[1])
    else:
        msb.showerror("Failed",result[1])
        

def get_reservation_data(event:Event):
    reservation_id=combo_reservation_id_view_reservation_window    .get().strip()
    result=connection.get_reservation_data(reservation_id)
    
    temp=[entry_username_view_reservation_window,entry_screen_id_view_reservation_window,entry_seat_count_view_reservation_window]
    clear_entries(temp)
    if result[0]==1:
        result=result[1]
        entry_username_view_reservation_window.insert(0,result[0])
        entry_screen_id_view_reservation_window.insert(0,result[1])
        entry_seat_count_view_reservation_window.insert(0,result[2])
    else: return


def update_reservation():
    reservation_id = combo_reservation_id_view_reservation_window   .get().strip()
    username = entry_username_view_reservation_window               .get().strip()
    screen_id = entry_screen_id_view_reservation_window             .get().strip()
    reserved_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        seat_count=int(entry_seat_count_reserve_movie_window.get().strip()) 
    except:
        msb.showerror("Invalid seat count","Enter a valid number!")
        return
    if reservation_id == "":
        msb.showerror('UpdatingError', 'You must choose or enter a valid ID reservation.')
        return
    
    if username == "" or screen_id == "" or seat_count == "":
        msb.showwarning("FormError", "You should change username, ID screen and seat counts correctly to submit an update for reservations.")
        return
    
    temp = connection.get_user_id(username)
    if temp[0] != 1:
        msb.showerror("Failed!", temp[1])
        return
    user_id_ = temp[1]
    

    result_screening_datetime = connection.get_screening_datetime(screen_id)
    if result_screening_datetime[0]==1:
        screening_datetime_str = result_screening_datetime[1].strftime("%Y-%m-%d %H:%M:%S")
        if reserved_at > screening_datetime_str:
            msb.showerror('UpdatingError', 'Screen time out!')
            return
    else:
        msb.showerror("Failed!",result_screening_datetime[1])
    
    result = connection.update_reservation(reservation_id, user_id_, screen_id, int(seat_count), reserved_at)
    if result[0] == 0:
        msb.showwarning("Couldn't update", result[1])
        return
    else:
        msb.showinfo("Successful update", result[1])


def delete_reservation():
    reservation_id=combo_reservation_id_view_reservation_window  .get().strip()
    screen_id=entry_screen_id_view_reservation_window            .get().strip() 
    if reservation_id=="" or screen_id=="":
        msb.showerror("RemovingError","Notice: We delete reservations according to their ID and ID screen.please enter these two variable correctly!")
        return 
    result=connection.delete_reservation(reservation_id,screen_id)
    
    if result[0]==0:
        msb.showerror("Failed to delete",result[1])
        return
    elif result[0]==-1:
        msb.showerror("Not found",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])
    

def insert_movie():
    movie_id=combo_movie_id_movie_window            .get().strip()
    title=entry_title_movie_window                  .get().strip()
    director=entry_director_movie_window            .get().strip()
    genre=entry_genre_movie_window                  .get().strip()
    duration=entry_duration_movie_window            .get().strip()
    release_date=entry_release_date_movie_window    .get().strip()
    rating=entry_rating_movie_window                .get().strip()
    
    if title=="" or director=="" or genre=="" or duration=="" or release_date=="" or rating=="":
        msb.showwarning("InsertError","Fill title,director,genre,duration,release date and rating to add a new movie!")
        return
    
    try:
        temp=datetime.strptime(release_date,'%Y-%m-%d %H:%M:%S')
        if temp>=datetime.now():
            msb.showwarning("Invalid datetime","You can't enter this datetime.")
            return    
    except:
        msb.showwarning("Invalid datetime","You can't enter this datetime.")
        return
    
        
    
    if movie_id=="":movie_id=None
    result=connection.insert_movie(title,director,genre,duration,release_date,rating,movie_id)
    if result[0]==0:
        msb.showerror("Addition faield",result[1])
    else:
        msb.showinfo("Successful",result[1])
            
    temp=[combo_movie_id_movie_window,entry_title_movie_window,entry_director_movie_window,entry_genre_movie_window,entry_duration_movie_window,entry_release_date_movie_window,entry_rating_movie_window]
    clear_entries(temp)
    search_movie()


def get_movie_data(event:Event):
    movie_id=combo_movie_id_movie_window    .get().strip()
    result=connection.get_movie_data(movie_id)
    
    temp=[entry_title_movie_window,entry_director_movie_window,entry_genre_movie_window,entry_duration_movie_window,entry_release_date_movie_window,entry_rating_movie_window]
    clear_entries(temp)
    if result[0]==1:
        result=result[1]
        for index,jk in enumerate(temp,start=1):
            jk:Entry
            jk.insert(0,result[index])
    else:return


def update_movie():
    movie_id=combo_movie_id_movie_window         .get().strip()
    title=entry_title_movie_window               .get().strip()
    director=entry_director_movie_window         .get().strip()
    genre=entry_genre_movie_window               .get().strip()
    duration=entry_duration_movie_window         .get().strip()
    release_date=entry_release_date_movie_window .get().strip()
    rating=entry_rating_movie_window             .get().strip()
  
    if movie_id=="" or title=="" or  director=="" or genre=="" or duration=="" or release_date=="" or rating=="":
        msb.showwarning("FormError","Fill all movie properties to update!")
        return
    
    result=connection.update_movie(movie_id,title,director,genre,duration,release_date,rating)
    if  result[0]==0:
        msb.showwarning("Couldn't update",result[1])
        return
    else:
        msb.showinfo("Successful update",result[1])
    temp=[combo_movie_id_movie_window,entry_title_movie_window,entry_director_movie_window,entry_genre_movie_window,entry_duration_movie_window,entry_release_date_movie_window,entry_rating_movie_window]
    clear_entries(temp)
    search_movie()   
  
        
def delete_movie():
    movie_id=combo_movie_id_movie_window    .get().strip()
    title=entry_title_movie_window          .get().strip()
    if movie_id=="" or title=="":
        msb.showerror("RemovingError","Notice: We delete movies according to their ID and Title.please enter these two variable correctly!")
        return 
    result=connection.delete_movie(movie_id,title)
    if result[0]==0:
        msb.showerror("Failed to delete",result[1])
        return
    elif result[0]==-1:
        msb.showerror("Not found",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])
    temp=[combo_movie_id_movie_window,entry_title_movie_window,entry_director_movie_window,entry_genre_movie_window,entry_duration_movie_window,entry_release_date_movie_window,entry_rating_movie_window]
    clear_entries(temp)
    search_movie()       


def search_movie():
    movie_id=combo_movie_id_movie_window         .get().strip()
    title=entry_title_movie_window               .get().strip()
    director=entry_director_movie_window         .get().strip()
    genre=entry_genre_movie_window               .get().strip()
    duration=entry_duration_movie_window         .get().strip()
    release_date=entry_release_date_movie_window .get().strip()
    rating=entry_rating_movie_window             .get().strip()

    result=connection.search_movie(movie_id,title,director,genre,duration,release_date,rating)
    if result[0]==0:
        msb.showerror("Failed!",result[1])
        return
    else:    
        result=result[1]
        treev_movie_window.delete(*treev_movie_window.get_children())
        for item in result:
            treev_movie_window.insert("",END,values=item)
 
      
def add_hall():
    name=entry_name_hall_window.get().strip()
    capacity=entry_capacity_hall_window.get().strip() 
    if name=="" or capacity=="":
        msb.showwarning("FormError","Enter hall name and capacity!")
        return
    try:
        capacity=int(capacity)
    except:
        msb.showerror("CapacityError","capacity number must be integer!")
        return
    result=connection.add_hall(name,capacity)
    if result[0]==0:
        msb.showerror("Addition failed",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])


def delete_hall():
    name=entry_name_hall_window.get().strip()    
    result=connection.delete_hall(name)
    if result[0]==0:
        msb.showerror("Failed to delete",result[1])
        return
    elif result[0]==-1:
        msb.showerror("Not found",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])


def reserve_ticket():
    global user_id,lst_entry_screen_info_reserve_movie_window
    try: 
        item=treev_screen_window.selection()
        selected_row=treev_screen_window.item(item)
        screen_id_selected_row=selected_row["values"][0]
        result=connection.reserve_ticket(screen_id_selected_row)
    except IndexError:
        msb.showerror("SelectionError","Select a row first!")
        return
    if result[0]==0:
        msb.showerror("Failed!",result[1])
        return
    else:
        lst_entry_screen_info_reserve_movie_window=[entry_screen_id_reserve_movie_window,
            entry_screening_datetime_reserve_movie_window,
            entry_hall_reserve_movie_window,
            entry_ticket_price_reserve_movie_window,
            entry_movie_reserve_movie_window,
            entry_director_reserve_movie_window,
            entry_duration_reserve_movie_window,
            entry_genre_reserve_movie_window,
            entry_release_date_reserve_movie_window,
            entry_rating_reserve_movie_window]
        change_window(screen_window,reserve_movie_window)
        result=result[1]
   
       
        for index,entry in enumerate(lst_entry_screen_info_reserve_movie_window):
            entry.insert(0,result[index])
            entry.config(state="readonly")


def check_and_reserve():
    global user_id
    screen_id = entry_screen_id_reserve_movie_window.get().strip()
    if screen_id == "":
        msb.showerror("Error", "No screen selected!")
        return
      
    try:
        seat_count=int(entry_seat_count_reserve_movie_window.get().strip()) 
    except:
        msb.showerror("Invalid seat count","Enter a valid number!")
        return
    result=connection.check_and_reserve(user_id,seat_count,screen_id)
    if result[0]==-1 or result[0]==0 or result[0]==-2:
        msb.showerror("Failed to reserve!",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])
        change_window(reserve_movie_window,screen_window)
        return    


def search_screen():
    global access_level 
    
    screen_id=combo_screen_id_screen_window                         .get().strip()
    movie=combo_movie_screen_window                                 .get().strip()
    hall=combo_hall_screen_window                                   .get().strip()
    screening_datetime=entry_screening_datetime_screen_window       .get().strip()
    ticket_price=entry_ticket_price_screen_window                   .get().strip()
    result=connection.search_screen(screen_id,access_level,movie,hall,screening_datetime,ticket_price)
    treev_screen_window.delete(*treev_screen_window.get_children())
    if result[0]==0 or result[0]==-1:
        msb.showerror("Failed",result[1])
        return   
    else:
        result=result[1]
        for item in result:
            treev_screen_window.insert("",END,values=item)
        

def add_screen():
    screen_id=combo_screen_id_screen_window                  .get().strip()
    movie=combo_movie_screen_window                          .get().strip()
    hall=combo_hall_screen_window                            .get().strip()
    screening_datetime=entry_screening_datetime_screen_window.get().strip()
    ticket_price=entry_ticket_price_screen_window            .get().strip()
    
    if movie=="" or hall=="" or screening_datetime=="" or ticket_price=="":
        msb.showerror("ScreenError","You must define movie,hall,screening datetime and ticket price!")
        return
    try:
        temp=datetime.strptime(screening_datetime,'%Y-%m-%d %H:%M:%S')
        if temp<datetime.now():
            msb.showwarning("Invalid datetime","You can't enter this datetime.")
            return    
    except:
        msb.showwarning("Invalid datetime","You can't enter this datetime.")
        return
    if screen_id=="": screen_id=None
    
    hall_free=connection .is_hall_free(hall,screening_datetime,movie)
    if not hall_free:
        msb.showwarning("Hall free checking went wrong!","May be Hall already reserved. or invalid data entered")
        return
    
    result=connection   .add_screen(movie,hall,screening_datetime,ticket_price,screen_id)
    if result[0]==0:
        msb.showerror("Failed!",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])
        return
  
        
def get_screen_data(event:Event):
    screen_id=combo_screen_id_screen_window    .get().strip()
    result=connection.get_screen_data(screen_id)
    if result[0]==1:
        entry_screening_datetime_screen_window   .delete(0,END)
        entry_ticket_price_screen_window         .delete(0,END)
        result=result[1]
        combo_movie_screen_window                 .set(result[1])
        combo_hall_screen_window                  .set(result[2])
        entry_screening_datetime_screen_window    .insert(0,result[3])
        entry_ticket_price_screen_window          .insert(0,result[4])
    else:
        msb.showerror("Failed to get data!",result[1])  


def update_screen():
    screen_id=combo_screen_id_screen_window                     .get().strip()
    movie=combo_movie_screen_window                             .get().strip()
    hall=combo_hall_screen_window                               .get().strip()
    screening_datetime=entry_screening_datetime_screen_window   .get().strip()
    ticket_price=entry_ticket_price_screen_window               .get().strip()
    
    if screen_id=="" or movie=="" or hall=="" or screening_datetime=="" or ticket_price=="":
        msb.showwarning("UpdatingError","For Updating a screen fill all the blanks, first.")
        return
    if screening_datetime<datetime.now().strftime("%Y-%m-%d %H:%M:%S"):
        msb.showwarning("Invalid datetime","You can't enter this datetime.")
        return 
    
    hall_free=connection    .is_hall_free(hall,screening_datetime,movie,screen_id)
    if not hall_free:
        msb.showwarning("Wrong hall selected","You can't enter this hall.\nHall already reserved.")
        return
    
    result=connection.update_screen(screen_id,movie,hall,screening_datetime,ticket_price)
    if result[0]==0:
        msb.showerror("UpdatingError",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])    
    
    
def delete_screen():
    screen_id=combo_screen_id_screen_window.get().strip()
    movie=combo_movie_screen_window.get().strip()
    if screen_id=="" or movie=="":
        msb.showerror("RemovingError","Notice: We delete screens according to their ID and movie.please enter these two variable correctly!")
        return 
    result=connection.delete_screen(screen_id,movie)
    if result[0]==0:
        msb.showerror("Failed to delete",result[1])
        return
    elif result[0]==-1:
        msb.showerror("Not found",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])


def search_user():
    user_id=combo_user_id_users_window.get().strip()
    name=entry_name_users_window.get().strip()
    surname=entry_surname_users_window.get().strip()
    username=combo_username_users_window.get().strip()
    access_level=combo_access_level_users_window.get().strip()
    
    result=connection.search_user(user_id,name,surname,username,access_level)
    treev_users_window.delete(*treev_users_window.get_children())        
    if result[0]==0:
        msb.showerror("Failed",result[1])
        return   
    else:
        result=result[1]
        for item in result:
            treev_users_window.insert("",END,values=item)


def get_user_data(event:Event):
    user_id=combo_user_id_users_window       .get().strip()
    result=connection.get_user_data(user_id)
    entry_name_users_window                  .delete(0,END)
    entry_surname_users_window               .delete(0,END)
    if result[0]!=1:
        msb.showerror("Failed!",result[1])
        return
    result=result[1]
    
    if result[1]!=None: 
        entry_name_users_window              .insert(0,result[1])
    else:entry_name_users_window             .insert(0,"")
    
    if result[2]!=None:
        entry_surname_users_window           .insert(0,result[2]) 
    else:entry_surname_users_window          .insert(0,"")
    
    # because name or surname can be None and we can't insert None into an entry.
    
    combo_username_users_window              .set(result[3])
    combo_access_level_users_window          .set(result[4])
    

def update_user():
    user_id=combo_user_id_users_window              .get().strip()
    name=entry_name_users_window                    .get().strip()
    surname=entry_surname_users_window              .get().strip()
    username=combo_username_users_window            .get().strip()
    access_level=combo_access_level_users_window    .get().strip()
    if user_id=="" or name=="" or surname=="" or username=="" or access_level=="" :
        msb.showwarning("UpdatingError","For Updating a user fill all the blanks,first.")
        return
    result=connection.update_user(user_id,name,surname,username,access_level)
    if result[0]==0:
        msb.showerror("UpdatingError",result[1])
        return
    else:
        msb.showinfo("Done!",result[1])    


def delete_user():
    user_id=combo_user_id_users_window      .get().strip()
    username=combo_username_users_window    .get().strip()
    if user_id=="" or username=="":
        msb.showerror("RemovingError","Notice: We delete users according to their ID and username.please enter these two variable correctly!")
        return 
    result=connection.delete_user(user_id,username)
    if result[0]==0:
        msb.showerror("Failed to delete",result[1])
        return
    elif result[0]==-1:
        msb.showerror("Not found",result[1])
        return
    else:
        msb.showinfo("Done!",result[1]) 


def edit_profile():
    global user_id,access_level
    name=entry_name_sign_up_window                      .get().strip()
    surname=entry_surname_sign_up_window                .get().strip()
    username=entry_username_sign_up_window              .get().strip()
    password=entry_password_sign_up_window              .get().strip()
    password2=entry_password2_sign_up_window            .get().strip()
    new_access_level=entry_access_level_sign_up_window  .get().strip()
    
    if username=="":
        msb.showwarning("UsernameError","username can't be empty!")
        return
    
    if len(password)<5:
        msb.showwarning("PasswordError","password must be at least 5 characters!")
        return
    
    if password!=password2:
        msb.showwarning("PasswordError","passwords don't match!")
        return
    
    
    
    if name=="":    name=None
    if surname=="": surname=None
    
    result=connection.edit_profile(user_id,access_level,name,surname,username,password,new_access_level)
    if result[0]==1:
        msb.showinfo("Done!",result[1])
        change_window(sign_up_window,main_menu)
    else:
        msb.showerror("Failed",result[1])
    
    temp=[entry_name_sign_up_window,entry_surname_sign_up_window,entry_username_sign_up_window,entry_password_sign_up_window,entry_password2_sign_up_window,entry_access_level_sign_up_window]
    clear_entries(temp)
    

############ ROOT WINDOW    
root=Tk()

#root.withdraw()
root.title("IRAN Cinema")
root.geometry("450x110+50+50")
root.resizable(False,False)
root.config(cnf=CNF_WINDOW)
photo_root=Image.open(r"Cinema booking system (tkinter)\Images\root_icon.jpg")
photo_root=ImageTk.PhotoImage(photo_root)
root.iconphoto(False,photo_root)

lbl_welcome_root    =Label(root,CNF_LBL_ROOT    ,text="Welcome to Cinema Booking Service!")
btn_sign_up_root    =Button(root,CNF_BTN_ROOT   ,text="Sign up",command=lambda:change_window(root,sign_up_window))
btn_login_root      =Button(root,CNF_BTN_ROOT   ,text="Login"  ,command=lambda:change_window(root,login_window))

lbl_welcome_root    .grid(CNF_GRID_GENERAL  ,row=1,column=1,columnspan=2)
btn_sign_up_root    .grid(CNF_GRID_BTN_ROOT ,row=2,column=1)
btn_login_root      .grid(CNF_GRID_BTN_ROOT ,row=2,column=2)

############# SIGN UP WINDOW 
sign_up_window=Toplevel(root)
sign_up_window.geometry("+50+50")
sign_up_window.resizable(False,False)
sign_up_window.withdraw()
sign_up_window.protocol("WM_DELETE_WINDOW",root.destroy)
sign_up_window.config(CNF_WINDOW)
photo_sign_up=Image.open(r"Cinema booking system (tkinter)\Images\sign_up_icon.png")
photo_sign_up=ImageTk.PhotoImage(photo_sign_up)
sign_up_window.iconphoto(False,photo_sign_up)

lbl_name_sign_up_window             =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Name: ")
lbl_surname_sign_up_window          =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Surname: ")
lbl_username_sign_up_window         =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Username: ")
lbl_password_sign_up_window         =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Password: ")
lbl_password2_sign_up_window        =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Repeat Password: ")
lbl_access_level_sign_up_window     =Label(sign_up_window,CNF_LBL_SIGN_UP_WINDOW,text="Access level: ")
entry_name_sign_up_window           =Entry(sign_up_window,CNF_ENTRY_GENERAL)
entry_surname_sign_up_window        =Entry(sign_up_window,CNF_ENTRY_GENERAL)
entry_username_sign_up_window       =Entry(sign_up_window,CNF_ENTRY_GENERAL)
entry_password_sign_up_window       =Entry(sign_up_window,CNF_ENTRY_GENERAL)
entry_password2_sign_up_window      =Entry(sign_up_window,CNF_ENTRY_GENERAL)
entry_access_level_sign_up_window   =Entry(sign_up_window,CNF_ENTRY_GENERAL)
btn_ok_sign_up_window               =Button(sign_up_window,CNF_BTN_SIGN_UP_WINDOW,text="OK"   ,command=insert_user)
btn_back_sign_up_window             =Button(sign_up_window,CNF_BTN_SIGN_UP_WINDOW,text="Back" )

lbl_name_sign_up_window             .grid(CNF_GRID_GENERAL,row=1,column=1)
lbl_surname_sign_up_window          .grid(CNF_GRID_GENERAL,row=2,column=1)
lbl_username_sign_up_window         .grid(CNF_GRID_GENERAL,row=3,column=1)
lbl_password_sign_up_window         .grid(CNF_GRID_GENERAL,row=4,column=1)
lbl_password2_sign_up_window        .grid(CNF_GRID_GENERAL,row=5,column=1)
entry_name_sign_up_window           .grid(CNF_GRID_GENERAL,row=1,column=2)
entry_surname_sign_up_window        .grid(CNF_GRID_GENERAL,row=2,column=2)
entry_username_sign_up_window       .grid(CNF_GRID_GENERAL,row=3,column=2)
entry_password_sign_up_window       .grid(CNF_GRID_GENERAL,row=4,column=2)
entry_password2_sign_up_window      .grid(CNF_GRID_GENERAL,row=5,column=2)
btn_back_sign_up_window             .grid(CNF_GRID_BTN_SIGN_UP_WINDOW,row=7,column=1)
btn_ok_sign_up_window               .grid(CNF_GRID_BTN_SIGN_UP_WINDOW,row=7,column=2)

################# LOGIN WINDOW
login_window=Toplevel(root)
login_window.geometry("+50+50")
login_window.resizable(False,False)
login_window.withdraw()
login_window.protocol("WM_DELETE_WINDOW",root.destroy)
login_window.title("Login window")
login_window.config(CNF_WINDOW)
photo_login=Image.open(r"Cinema booking system (tkinter)\Images\login_icon.png")
photo_login=ImageTk.PhotoImage(photo_login)
login_window.iconphoto(False,photo_login)

lbl_username_login_window   =Label(login_window,CNF_LBL_LOGIN_WINDOW    ,text="Username: ")
lbl_password_login_window   =Label(login_window,CNF_LBL_LOGIN_WINDOW    ,text="Password: ")
entry_username_login_window =Entry(login_window,CNF_ENTRY_GENERAL)
entry_password_login_window =Entry(login_window,CNF_ENTRY_GENERAL       ,show="*")
btn_login_window            =Button(login_window,CNF_BTN_LOGIN_WINDOW   ,text="Login" ,command=login)
btn_back_login_window       =Button(login_window,CNF_BTN_LOGIN_WINDOW   ,text="Back"  ,command=lambda:change_window(login_window,root))

lbl_username_login_window   .grid(CNF_GRID_GENERAL,row=1,column=1)
lbl_password_login_window   .grid(CNF_GRID_GENERAL,row=2,column=1)
entry_username_login_window .grid(CNF_GRID_GENERAL,row=1,column=2)
entry_password_login_window .grid(CNF_GRID_GENERAL,row=2,column=2)
btn_login_window            .grid(CNF_GRID_GENERAL,row=3,column=1)
btn_back_login_window       .grid(CNF_GRID_GENERAL,row=3,column=2,sticky="e",padx=20)

##################### MAIN MENU 
main_menu=Toplevel(root)
main_menu.geometry("+50+50")
main_menu.resizable(False,False)
main_menu.withdraw()
main_menu.protocol("WM_DELETE_WINDOW",root.destroy)
main_menu.title("Main menu")
main_menu.config(CNF_WINDOW)
photo_main_menu=Image.open(r"Cinema booking system (tkinter)\Images\main_menu_icon.png")
photo_main_menu=ImageTk.PhotoImage(photo_main_menu)
main_menu.iconphoto(False,photo_main_menu)

btn_view_reservation_main_menu      =Button(main_menu,CNF_BTN_MAIN_MENU                             ,command=lambda:change_window(main_menu,view_reservation_window))
btn_manage_movies_main_menu         =Button(main_menu,CNF_BTN_MAIN_MENU,text="Movies"               ,command=lambda:change_window(main_menu,movie_window))
btn_manage_halls_main_menu          =Button(main_menu,CNF_BTN_MAIN_MENU,text=" Halls"               ,command=lambda:change_window(main_menu,hall_window))
btn_manage_screens_main_menu        =Button(main_menu,CNF_BTN_MAIN_MENU,text=" Screens"             ,command=lambda:change_window(main_menu,screen_window))
btn_manage_users_main_menu          =Button(main_menu,CNF_BTN_MAIN_MENU,text=" Users"               ,command=lambda:change_window(main_menu,users_window))
btn_profile_main_menu               =Button(main_menu,CNF_BTN_MAIN_MENU,text=" My Profile"          ,command=lambda:change_window(main_menu,sign_up_window))
btn_log_out_main_menu               =Button(main_menu,CNF_BTN_MAIN_MENU,text="Log Out"              ,command=lambda:change_window(main_menu,login_window))

btn_view_reservation_main_menu      .grid(CNF_GRID_GENERAL,row=1,column=1)
btn_manage_screens_main_menu        .grid(CNF_GRID_GENERAL,row=4,column=1)
btn_profile_main_menu               .grid(CNF_GRID_GENERAL,row=7,column=1)
btn_log_out_main_menu               .grid(CNF_GRID_GENERAL,row=8,column=1)

################# RESERVATION WINDOW
view_reservation_window=Toplevel(root)
view_reservation_window.resizable(False,False)
view_reservation_window.withdraw()
view_reservation_window.protocol("WM_DELETE_WINDOW",root.destroy)
view_reservation_window.title("Reservation window")
view_reservation_window.config(CNF_WINDOW)
photo_view_reservation=Image.open(r"Cinema booking system (tkinter)\Images\view_reservation_icon.png")
photo_view_reservation=ImageTk.PhotoImage(photo_view_reservation)
view_reservation_window.iconphoto(False,photo_view_reservation)


treev_view_reservation_window   =ttk.Treeview(view_reservation_window   ,show="headings",selectmode="browse",columns=["1","2","3","4","5","6","7","8","9","10","11","12"])
scr_view_reservation_window     =Scrollbar(view_reservation_window      ,orient="vertical",command=treev_view_reservation_window.yview)
treev_view_reservation_window   .config(yscrollcommand=scr_view_reservation_window.set)

columns_treev_view_reservation_window   =["ID reservation","Username","ID screen","Seats count","Reserved at","Ticket price","Screening datetime","Hall","Movie","Director","Duration","Rating"]
for p in range(12):
    treev_view_reservation_window.heading(f"{p+1}",text=columns_treev_view_reservation_window[p])

width_treev_view_reservation_window     =["85","130","70","70","150","100","150","130","160","140","70","70"]
for q in range(12):
    treev_view_reservation_window.column(f"{q+1}",width=width_treev_view_reservation_window[q],anchor="center")

frame_options_reservation_window    =LabelFrame(view_reservation_window,CNF_LABLE_FRAME,text="Reservation Options")
frame_btn_reservation_window        =Frame(view_reservation_window,CNF_FRAME)

for e in range(4):
    for w in range(3):
        Label(frame_options_reservation_window,CNF_LBL_VIEW_RESERVATION_WINDOW,text=columns_treev_view_reservation_window[3*e+w]+": ")   .grid(CNF_GRID_GENERAL,row=e+1,column=2*w+1,sticky="w")

combo_reservation_id_view_reservation_window    =ttk.Combobox(frame_options_reservation_window,width=40)
combo_reservation_id_view_reservation_window    .bind("<<ComboboxSelected>>",get_reservation_data)
entry_username_view_reservation_window          =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_screen_id_view_reservation_window         =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_seat_count_view_reservation_window        =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_reserved_at_view_reservation_window       =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_ticket_price_view_reservation_window      =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_screening_datetime_view_reservation_window=Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_hall_view_reservation_window              =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_movie_view_reservation_window             =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_director_view_reservation_window          =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_duration_view_reservation_window          =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)
entry_rating_view_reservation_window            =Entry(frame_options_reservation_window,CNF_ENTRY_GENERAL)

btn_search_refresh_view_reservation_window      =Button(frame_btn_reservation_window,CNF_BTN_VIEW_RESERVATION_WINDOW,text="Search & refresh"    ,command=search_reservation)
btn_add_view_reservation_window                 =Button(frame_btn_reservation_window,CNF_BTN_VIEW_RESERVATION_WINDOW,text="Add reservation"     ,command=add_reservation)
btn_update_view_reservation_window              =Button(frame_btn_reservation_window,CNF_BTN_VIEW_RESERVATION_WINDOW,text="Update reservation"  ,command=update_reservation)
btn_delete_view_reservation_window              =Button(frame_btn_reservation_window,CNF_BTN_VIEW_RESERVATION_WINDOW,text="Delete reservation"  ,command=delete_reservation)
btn_back_view_reservation_window                =Button(frame_btn_reservation_window,CNF_BTN_VIEW_RESERVATION_WINDOW,text="Back"                ,command=lambda:change_window(view_reservation_window,main_menu))

treev_view_reservation_window                   .grid(CNF_GRID_GENERAL,row=1,column=1,sticky="news")
scr_view_reservation_window                     .grid(CNF_GRID_GENERAL,row=1,column=2,sticky="ns")
frame_options_reservation_window                .grid(CNF_GRID_GENERAL,row=2,column=1,sticky="n")
frame_btn_reservation_window                    .grid(CNF_GRID_GENERAL,row=3,column=1,sticky="n")
combo_reservation_id_view_reservation_window    .grid(CNF_GRID_GENERAL,row=1,column=2)
entry_username_view_reservation_window          .grid(CNF_GRID_GENERAL,row=1,column=4)
entry_screen_id_view_reservation_window         .grid(CNF_GRID_GENERAL,row=1,column=6)
entry_seat_count_view_reservation_window        .grid(CNF_GRID_GENERAL,row=2,column=2)                
entry_reserved_at_view_reservation_window       .grid(CNF_GRID_GENERAL,row=2,column=4)
entry_ticket_price_view_reservation_window      .grid(CNF_GRID_GENERAL,row=2,column=6)
entry_screening_datetime_view_reservation_window.grid(CNF_GRID_GENERAL,row=3,column=2)
entry_hall_view_reservation_window              .grid(CNF_GRID_GENERAL,row=3,column=4)
entry_movie_view_reservation_window             .grid(CNF_GRID_GENERAL,row=3,column=6)
entry_director_view_reservation_window          .grid(CNF_GRID_GENERAL,row=4,column=2)
entry_duration_view_reservation_window          .grid(CNF_GRID_GENERAL,row=4,column=4)
entry_rating_view_reservation_window            .grid(CNF_GRID_GENERAL,row=4,column=6)
btn_search_refresh_view_reservation_window      .grid(CNF_GRID_GENERAL,row=1,column=1)

btn_delete_view_reservation_window              .grid(CNF_GRID_GENERAL,row=1,column=4)
btn_back_view_reservation_window                .grid(CNF_GRID_GENERAL,row=1,column=5)

################## MOVIE WINDOW 
movie_window=Toplevel(root)
movie_window.geometry("+50+50")
movie_window.resizable(False,False)
movie_window.withdraw()
movie_window.protocol("WM_DELETE_WINDOW",root.destroy)
movie_window.title("Movie window")
movie_window.config(CNF_WINDOW)
photo_movie=Image.open(r"Cinema booking system (tkinter)\Images\movie_icon.png")
photo_movie=ImageTk.PhotoImage(photo_movie)
movie_window.iconphoto(False,photo_movie)

lbl_movie_id_movie_window        =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="ID movie: ")
lbl_title_movie_window           =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Title: ")
lbl_director_movie_window        =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Director: ")
lbl_genre_movie_window           =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Genre: ")
lbl_duration_movie_window        =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Duration: ")
lbl_release_date_movie_window    =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Release date: ")
lbl_rating_movie_window          =Label(movie_window,CNF_LBL_MOVIE_WINDOW,text="Rating: ")
combo_movie_id_movie_window      =ttk.Combobox(movie_window,width=40)
combo_movie_id_movie_window      .bind("<<ComboboxSelected>>",get_movie_data)
entry_title_movie_window         =Entry(movie_window,CNF_ENTRY_GENERAL)
entry_director_movie_window      =Entry(movie_window,CNF_ENTRY_GENERAL)
entry_genre_movie_window         =Entry(movie_window,CNF_ENTRY_GENERAL)
entry_duration_movie_window      =Entry(movie_window,CNF_ENTRY_GENERAL)
entry_release_date_movie_window  =Entry(movie_window,CNF_ENTRY_GENERAL)
entry_rating_movie_window        =Entry(movie_window,CNF_ENTRY_GENERAL)
btn_add_movie_window             =Button(movie_window,CNF_BTN_MOVIE_WINDOW,text="Add movie"                ,command=insert_movie)
btn_search_movie_window          =Button(movie_window,CNF_BTN_MOVIE_WINDOW,text="Search & refresh movies"  ,command=search_movie)
btn_update_movie_window          =Button(movie_window,CNF_BTN_MOVIE_WINDOW,text="Update movie"             ,command=update_movie)
btn_delete_movie_window          =Button(movie_window,CNF_BTN_MOVIE_WINDOW,text="Delete movie"             ,command=delete_movie)
btn_back_movie_window            =Button(movie_window,CNF_BTN_MOVIE_WINDOW,text="Back"                     ,command=lambda:change_window(movie_window,main_menu))

treev_movie_window               =ttk.Treeview(movie_window,columns=["1","2","3","4","5","6","7"],show="headings",selectmode="browse")
scr_movie_window                 =Scrollbar(movie_window,orient="vertical",command=treev_movie_window.yview)
treev_movie_window               .config(yscrollcommand=scr_movie_window.set)

columns_treev_movie_window=["ID movie","Title","Director","Genre","Duration","Release date","Rating"]
for m in range(7):
    treev_movie_window.heading(f"{m+1}",text=columns_treev_movie_window[m])

width_treev_movie_window=["70","150","130","130","70","150","70"]
for n in range(7):
    treev_movie_window.column(f"{n+1}",width=width_treev_movie_window[n],anchor="center")


lbl_movie_id_movie_window        .grid(CNF_GRID_GENERAL,row=1,column=1)
lbl_title_movie_window           .grid(CNF_GRID_GENERAL,row=2,column=1)
lbl_director_movie_window        .grid(CNF_GRID_GENERAL,row=3,column=1)
lbl_genre_movie_window           .grid(CNF_GRID_GENERAL,row=4,column=1)
lbl_duration_movie_window        .grid(CNF_GRID_GENERAL,row=5,column=1)
lbl_release_date_movie_window    .grid(CNF_GRID_GENERAL,row=6,column=1,sticky="n")
lbl_rating_movie_window          .grid(CNF_GRID_GENERAL,row=7,column=1,sticky="n")
combo_movie_id_movie_window      .grid(CNF_GRID_GENERAL,row=1,column=2)
entry_title_movie_window         .grid(CNF_GRID_GENERAL,row=2,column=2)
entry_director_movie_window      .grid(CNF_GRID_GENERAL,row=3,column=2)
entry_genre_movie_window         .grid(CNF_GRID_GENERAL,row=4,column=2)
entry_duration_movie_window      .grid(CNF_GRID_GENERAL,row=5,column=2)
entry_release_date_movie_window  .grid(CNF_GRID_GENERAL,row=6,column=2)
entry_rating_movie_window        .grid(CNF_GRID_GENERAL,row=7,column=2,sticky="n")
btn_add_movie_window             .grid(CNF_GRID_BTN_MOVIE_WINDOW,row=7,column=4,sticky="nw")
btn_search_movie_window          .grid(CNF_GRID_BTN_MOVIE_WINDOW,row=7,column=4,sticky="ne")
btn_update_movie_window          .grid(CNF_GRID_BTN_MOVIE_WINDOW,row=8,column=4,sticky="nw")
btn_delete_movie_window          .grid(CNF_GRID_BTN_MOVIE_WINDOW,row=8,column=4,sticky="ne")
btn_back_movie_window            .grid(CNF_GRID_BTN_MOVIE_WINDOW,row=8,column=1,sticky="n")
treev_movie_window               .grid(CNF_GRID_GENERAL,row=1,column=4,rowspan=7,sticky="n",pady=12)
scr_movie_window                 .grid(CNF_GRID_GENERAL,row=1,column=5,sticky="ns",rowspan=6)

###################### HALL WINDOW 
hall_window=Toplevel(root)
hall_window.geometry("+50+50")
hall_window.resizable(False,False)
hall_window.withdraw()
hall_window.protocol("WM_DELETE_WINDOW",root.destroy)
hall_window.title("Hall window")
hall_window.config(CNF_WINDOW)
photo_hall=Image.open(r"Cinema booking system (tkinter)\Images\hall_icon.png")
photo_hall=ImageTk.PhotoImage(photo_hall)
hall_window.iconphoto(False,photo_hall)

lbl_name_hall_window         =Label(hall_window,CNF_LBL_HALL_WINDOW    ,text="Name: ")
lbl_capacity_hall_window     =Label(hall_window,CNF_LBL_HALL_WINDOW    ,text="Capacity: ")
entry_name_hall_window       =Entry(hall_window,CNF_ENTRY_GENERAL)
entry_capacity_hall_window   =Entry(hall_window,CNF_ENTRY_GENERAL)
btn_add_hall_window          =Button(hall_window,CNF_BTN_HALL_WINDOW   ,text="Add hall"    ,command=add_hall)
btn_delete_hall_window       =Button(hall_window,CNF_BTN_HALL_WINDOW   ,text="Delete hall" ,command=delete_hall)
btn_back_hall_window         =Button(hall_window,CNF_BTN_HALL_WINDOW   ,text="Back"        ,command=lambda:change_window(hall_window,main_menu))
lbl_list_hall_window         =Label(hall_window,CNF_LBL_HALL_WINDOW    ,text="The List of halls: ")
combo_list_hall_window       =ttk.Combobox(hall_window,state="readonly",width=32)

lbl_name_hall_window        .grid(CNF_GRID_GENERAL              ,row=1,column=1)
lbl_capacity_hall_window    .grid(CNF_GRID_GENERAL              ,row=2,column=1)
entry_name_hall_window      .grid(CNF_GRID_ENTRY_HALL_WINDOW    ,row=1,column=2)
entry_capacity_hall_window  .grid(CNF_GRID_ENTRY_HALL_WINDOW    ,row=2,column=2)
btn_add_hall_window         .grid(CNF_GRID_GENERAL              ,row=3,column=1)
btn_delete_hall_window      .grid(CNF_GRID_GENERAL              ,row=3,column=2)
btn_back_hall_window        .grid(CNF_GRID_GENERAL              ,row=3,column=3,columnspan=2,sticky="w")
lbl_list_hall_window        .grid(CNF_GRID_GENERAL              ,row=4,column=1,columnspan=2,sticky="w")
combo_list_hall_window      .grid(CNF_GRID_GENERAL              ,row=4,column=3,columnspan=2,sticky="w")

######################## SCREEN WINDOW
screen_window=Toplevel(root)
screen_window.geometry("+50+50")
screen_window.resizable(False,False)
screen_window.withdraw()
screen_window.protocol("WM_DELETE_WINDOW",root.destroy)
screen_window.title("Screen window")
screen_window.config(CNF_WINDOW)
photo_screen=Image.open(r"Cinema booking system (tkinter)\Images\screen_icon.png")
photo_screen=ImageTk.PhotoImage(photo_screen)
screen_window.iconphoto(False,photo_screen)

treev_screen_window                     =ttk.Treeview(screen_window,columns=["1","2","3","4","5","6","7"],show="headings",selectmode="browse")
scr_screen_window                       =Scrollbar   (screen_window,orient="vertical",command=treev_screen_window.yview)
treev_screen_window                     .config      (yscrollcommand=scr_screen_window.set)

columns_treev_screen_window=["ID screen","Screening datetime","Ticket price","Movie","Director","Duration","Hall"]
for k in range(7):
    treev_screen_window.heading(f"{k+1}",text=columns_treev_screen_window[k])

width_treev_screen_window=["70","130","70","140","130","70","130"]
for l in range(7):
    treev_screen_window.column(f"{l+1}",width=width_treev_screen_window[l],anchor="center")

lbl_screen_id_manage_screen_window              =Label(screen_window,CNF_LBL_SCREEN_WINDOW,text="ID screen: ")
lbl_movie_manage_screen_window                  =Label(screen_window,CNF_LBL_SCREEN_WINDOW,text="Movie: ")
lbl_hall_manage_screen_window                   =Label(screen_window,CNF_LBL_SCREEN_WINDOW,text="Hall: ")
lbl_screening_datetime_manage_screen_window     =Label(screen_window,CNF_LBL_SCREEN_WINDOW,text="Screening datetime: ")
lbl_ticket_price_manage_screen_window           =Label(screen_window,CNF_LBL_SCREEN_WINDOW,text="Ticket price: ")
combo_screen_id_screen_window                   =ttk.Combobox(screen_window,width=40)
combo_screen_id_screen_window                   .bind("<<ComboboxSelected>>",get_screen_data)
combo_movie_screen_window                       =ttk.Combobox(screen_window,width=40,state="readonly")
combo_hall_screen_window                        =ttk.Combobox(screen_window,width=40,state="readonly")
entry_screening_datetime_screen_window          =Entry(screen_window,CNF_ENTRY_GENERAL)
entry_ticket_price_screen_window                =Entry(screen_window,CNF_ENTRY_GENERAL)
btn_reserve_ticket_screen_window                =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Reserve Ticket"           ,command=reserve_ticket)
btn_add_screen_screen_window                    =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Add Screen"               ,command=add_screen)
btn_update_screen_screen_window                 =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Update Screen"            ,command=update_screen)
btn_delete_screen_screen_window                 =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Delete Screen"            ,command=delete_screen)
btn_search_refresh_screens_screen_window        =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Search & Refresh Screen"  ,command=search_screen,font=("tahoma",13,"bold"),width=19)
btn_back_screen_window                          =Button(screen_window,CNF_BTN_SCREEN_WINDOW,text="Back"                     ,command=lambda:change_window(screen_window,main_menu))


treev_screen_window                             .grid(CNF_GRID_GENERAL          ,row=1,column=1,sticky="news")
scr_screen_window                               .grid(CNF_GRID_GENERAL          ,row=1,column=2,sticky="ns")
lbl_screen_id_manage_screen_window              .grid(CNF_GRID_LBL_SCREEN_WINDOW,row=2,column=1)
lbl_movie_manage_screen_window                  .grid(CNF_GRID_LBL_SCREEN_WINDOW,row=3,column=1)
lbl_hall_manage_screen_window                   .grid(CNF_GRID_LBL_SCREEN_WINDOW,row=4,column=1)
lbl_screening_datetime_manage_screen_window     .grid(CNF_GRID_LBL_SCREEN_WINDOW,row=5,column=1)
lbl_ticket_price_manage_screen_window           .grid(CNF_GRID_LBL_SCREEN_WINDOW,row=6,column=1)
combo_screen_id_screen_window                   .grid(CNF_GRID_GENERAL          ,row=2,column=1)
combo_movie_screen_window                       .grid(CNF_GRID_GENERAL          ,row=3,column=1)
combo_hall_screen_window                        .grid(CNF_GRID_GENERAL          ,row=4,column=1)
entry_screening_datetime_screen_window          .grid(CNF_GRID_GENERAL          ,row=5,column=1)
entry_ticket_price_screen_window                .grid(CNF_GRID_GENERAL          ,row=6,column=1)
btn_search_refresh_screens_screen_window        .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=5,column=1)
btn_back_screen_window                          .grid(CNF_GRID_BTN_SCREEN_WINDOW,row=6,column=1)

############## RESERVE MOVIE WINDOW
reserve_movie_window=Toplevel(root)
reserve_movie_window.geometry("+50+50")
reserve_movie_window.resizable(False,False)
reserve_movie_window.withdraw()
reserve_movie_window.protocol("WM_DELETE_WINDOW",root.destroy)
reserve_movie_window.title("Reserve movie window")
reserve_movie_window.config(CNF_WINDOW)
photo_reserve=Image.open(r"Cinema booking system (tkinter)\Images\reserve_icon.png")
photo_reserve=ImageTk.PhotoImage(photo_reserve)
reserve_movie_window.iconphoto(False,photo_reserve)

lbl_screen_info_reserve_movie_window            =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Screen Information: ")
lbl_screen_id_reserve_movie_window              =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="ID screen: ")
lbl_screening_datetime_reserve_movie_window     =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Screening datetime: ")
lbl_hall_reserve_movie_window                   =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Hall: ")
lbl_ticket_price_reserve_movie_window           =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Ticket price: ")
entry_screen_id_reserve_movie_window            =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_screening_datetime_reserve_movie_window   =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_hall_reserve_movie_window                 =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_ticket_price_reserve_movie_window         =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="_____________________________________________").grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=6,column=1,padx=3)

lbl_movie_reserve_movie_window                  =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Movie: ")
lbl_director_reserve_movie_window               =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Director: ")
lbl_duration_reserve_movie_window               =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Duration: ")
lbl_genre_reserve_movie_window                  =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Genre")
lbl_release_date_reserve_movie_window           =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Release date: ")
lbl_rating_reserve_movie_window                 =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="Rating: ")
entry_movie_reserve_movie_window                =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_director_reserve_movie_window             =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_duration_reserve_movie_window             =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_genre_reserve_movie_window                =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_release_date_reserve_movie_window         =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
entry_rating_reserve_movie_window               =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW,text="_____________________________________________").grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=13,column=1,padx=3)

lbl_seat_count_reserve_movie_window             =Label(reserve_movie_window,CNF_LBL_RESERVE_MOVIE_WINDOW ,text="Enter seat count: ", font=("tahoma",16,"bold"))
entry_seat_count_reserve_movie_window           =Entry(reserve_movie_window,CNF_ENTRY_GENERAL)
btn_ok_reserve_movie_window                     =Button(reserve_movie_window,CNF_BTN_RESERVE_MOVIE_WINDOW ,text="Ok"    ,command=check_and_reserve)
btn_back_reserve_movie_window                   =Button(reserve_movie_window,CNF_BTN_RESERVE_MOVIE_WINDOW ,text="Back"  ,command=lambda:change_window(reserve_movie_window,screen_window))

lbl_screen_info_reserve_movie_window            .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=1,column=1,padx=3)
lbl_screen_id_reserve_movie_window              .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=2,column=1)
lbl_screening_datetime_reserve_movie_window     .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=3,column=1)
lbl_hall_reserve_movie_window                   .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=4,column=1)
lbl_ticket_price_reserve_movie_window           .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=5,column=1)
lbl_movie_reserve_movie_window                  .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=7,column=1)
lbl_director_reserve_movie_window               .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=8,column=1)
lbl_duration_reserve_movie_window               .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=9,column=1)
lbl_genre_reserve_movie_window                  .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=10,column=1)
lbl_release_date_reserve_movie_window           .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=11,column=1)
lbl_rating_reserve_movie_window                 .grid(CNF_GRID_LBL_RESERVE_MOVIE_WINDOW,row=12,column=1)
entry_screen_id_reserve_movie_window            .grid(CNF_GRID_GENERAL                 ,row=2,column=2)
entry_screening_datetime_reserve_movie_window   .grid(CNF_GRID_GENERAL                 ,row=3,column=2)
entry_hall_reserve_movie_window                 .grid(CNF_GRID_GENERAL                 ,row=4,column=2)
entry_ticket_price_reserve_movie_window         .grid(CNF_GRID_GENERAL                 ,row=5,column=2)
entry_movie_reserve_movie_window                .grid(CNF_GRID_GENERAL                 ,row=7,column=2)
entry_director_reserve_movie_window             .grid(CNF_GRID_GENERAL                 ,row=8,column=2)
entry_duration_reserve_movie_window             .grid(CNF_GRID_GENERAL                 ,row=9,column=2)
entry_genre_reserve_movie_window                .grid(CNF_GRID_GENERAL                 ,row=10,column=2)
entry_release_date_reserve_movie_window         .grid(CNF_GRID_GENERAL                 ,row=11,column=2)
entry_rating_reserve_movie_window               .grid(CNF_GRID_GENERAL                 ,row=12,column=2)
lbl_seat_count_reserve_movie_window             .grid(CNF_GRID_GENERAL                 ,row=14,column=1)
entry_seat_count_reserve_movie_window           .grid(CNF_GRID_GENERAL                 ,row=14,column=2)
btn_ok_reserve_movie_window                     .grid(CNF_GRID_BTN_RESERVE_MOVIE_WINDOW,row=15,column=2)
btn_back_reserve_movie_window                   .grid(CNF_GRID_BTN_RESERVE_MOVIE_WINDOW,row=15,column=1)

################# USERS WINDOW
users_window=Toplevel(root)
users_window.geometry("+50+50")
users_window.resizable(False,False)
users_window.withdraw()
users_window.protocol("WM_DELETE_WINDOW",root.destroy)
users_window.title("Users window")
users_window.config(CNF_WINDOW)
photo_users=Image.open(r"Cinema booking system (tkinter)\Images\users_icon.png")
photo_users=ImageTk.PhotoImage(photo_users)
users_window.iconphoto(False,photo_users)

treev_users_window                     =ttk.Treeview(users_window,columns=["1","2","3","4","5"],show="headings",selectmode="browse")
scr_users_window                       =Scrollbar   (users_window,orient="vertical",command=treev_users_window.yview)
treev_users_window                     .config      (yscrollcommand=scr_users_window.set)

columns_treev_users_window=["ID user","Name","Surname","Username","Access level"]
for r in range(5):
    treev_users_window.heading(f"{r+1}",text=columns_treev_users_window[r])

width_treev_users_window=["65","120","170","150","75"]
for u in range(5):
    treev_users_window.column(f"{u+1}",width=width_treev_users_window[u],anchor="center")

frame_options_users_window      =LabelFrame(users_window,CNF_LABLE_FRAME,text="Users options")
frame_btn_users_window          =Frame(users_window,CNF_FRAME)
lbl_user_id_users_window        =Label(frame_options_users_window,CNF_LBL_USERS_WINDOW,text="ID user")
lbl_name_users_window           =Label(frame_options_users_window,CNF_LBL_USERS_WINDOW,text="Name")
lbl_surname_users_window        =Label(frame_options_users_window,CNF_LBL_USERS_WINDOW,text="Surname")
lbl_username_users_window       =Label(frame_options_users_window,CNF_LBL_USERS_WINDOW,text="Username")
lbl_access_level_users_window   =Label(frame_options_users_window,CNF_LBL_USERS_WINDOW,text="Access level")
combo_user_id_users_window      =ttk.Combobox(frame_options_users_window,width=40)
combo_user_id_users_window      .bind("<<ComboboxSelected>>",get_user_data)
entry_name_users_window         =Entry(frame_options_users_window,CNF_ENTRY_GENERAL)
entry_surname_users_window      =Entry(frame_options_users_window,CNF_ENTRY_GENERAL)
combo_username_users_window     =ttk.Combobox(frame_options_users_window,width=40)
combo_access_level_users_window =ttk.Combobox(frame_options_users_window,width=40,values=["",1,2],state="readonly")

btn_search_refresh_users_window =Button(frame_btn_users_window,CNF_BTN_USERS_WINDOW,text="Search & refresh" ,command=search_user)
btn_add_users_window            =Button(frame_btn_users_window,CNF_BTN_USERS_WINDOW,text="Add user"         ,command=lambda:change_window(users_window,sign_up_window))
btn_update_users_window         =Button(frame_btn_users_window,CNF_BTN_USERS_WINDOW,text="Update user"      ,command=update_user)
btn_delete_users_window         =Button(frame_btn_users_window,CNF_BTN_USERS_WINDOW,text="Delete user"      ,command=delete_user)
btn_back_users_window           =Button(frame_btn_users_window,CNF_BTN_USERS_WINDOW,text="Back"             ,command=lambda:change_window(users_window,main_menu))


treev_users_window              .grid(CNF_GRID_GENERAL,row=1,column=1,sticky="news")
scr_users_window                .grid(CNF_GRID_GENERAL,row=1,column=2,sticky="ns")
frame_options_users_window      .grid(CNF_GRID_GENERAL,row=2,column=1,sticky="n")
frame_btn_users_window          .grid(CNF_GRID_GENERAL,row=3,column=1,sticky="n")
lbl_user_id_users_window        .grid(CNF_GRID_GENERAL,row=1,column=1)
lbl_name_users_window           .grid(CNF_GRID_GENERAL,row=1,column=3)
lbl_surname_users_window        .grid(CNF_GRID_GENERAL,row=2,column=1)
lbl_username_users_window       .grid(CNF_GRID_GENERAL,row=2,column=3)
lbl_access_level_users_window   .grid(CNF_GRID_GENERAL,row=3,column=1)
combo_user_id_users_window      .grid(CNF_GRID_GENERAL,row=1,column=2)
entry_name_users_window         .grid(CNF_GRID_GENERAL,row=1,column=4)
entry_surname_users_window      .grid(CNF_GRID_GENERAL,row=2,column=2)
combo_username_users_window     .grid(CNF_GRID_GENERAL,row=2,column=4)
combo_access_level_users_window .grid(CNF_GRID_GENERAL,row=3,column=2)
btn_search_refresh_users_window .grid(CNF_GRID_GENERAL,row=1,column=1)
btn_add_users_window            .grid(CNF_GRID_GENERAL,row=1,column=2)
btn_update_users_window         .grid(CNF_GRID_GENERAL,row=1,column=3)
btn_delete_users_window         .grid(CNF_GRID_GENERAL,row=1,column=4)
btn_back_users_window           .grid(CNF_GRID_GENERAL,row=1,column=5)
#################

try:
    mainloop()
except:exit()
    
    