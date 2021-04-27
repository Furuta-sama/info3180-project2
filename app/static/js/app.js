/* Add your Application JavaScript */
Vue.component('app-header', {
    template: `
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary fixed-top">
      <a class="navbar-brand" href="/"> <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 0 24 24" width="24px" fill="#FFFFFF"><path d="M0 0h24v24H0z" fill="none"/><path d="M18.92 6.01C18.72 5.42 18.16 5 17.5 5h-11c-.66 0-1.21.42-1.42 1.01L3 12v8c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-1h12v1c0 .55.45 1 1 1h1c.55 0 1-.45 1-1v-8l-2.08-5.99zM6.5 16c-.83 0-1.5-.67-1.5-1.5S5.67 13 6.5 13s1.5.67 1.5 1.5S7.33 16 6.5 16zm11 0c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zM5 11l1.5-4.5h11L19 11H5z"/></svg> United Auto Sales</a>
      <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
    
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <ul class="navbar-nav ml-auto">
          <li class="nav-item active">
            <router-link class="nav-link" to="/cars/new">Add Car <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
            <router-link class="nav-link" to="/explore">Explore <span class="sr-only">(current)</span></router-link>
          </li>
          <li class="nav-item active">
            <router-link class="nav-link" @click="profile()" v-bind:to="'/users/' + c_user">My Profile <span class="sr-only">(current)</span></router-link>
          </li>
          <li v-if="!status_log" class="nav-item active">
            <router-link class="nav-link" to="/login">Login <span class="sr-only">(current)</span></router-link>
          </li>
          <li v-else class="nav-item active">
            <router-link class="nav-link" to="/logout">Logout <span class="sr-only">(current)</span></router-link>
          </li>
        </ul>
      </div>
    </nav>
    `,

    computed: {
        status_log: function() {
            if (sessionStorage.getItem('token')) {
                return true;
            } else {
                return false;
            }
        }
    },

    methods: {
        profile: function(){ 
            //this.$router.push("/users/"+userid)
            location.reload();
        }
    },

    data: function(){
        return {
            c_user: 0
        }
    },

    created: function(){
        let self = this;
        fetch('/api/secure', {
            'headers': {
                'Authorization': 'Bearer ' + sessionStorage.getItem('token')
            }
        }).then(function (response) {
                return response.json();
            }).then(function (response) {
                let result = response.data;
                console.log("User ID retrieved");
                self.c_user = result.user.id;
                //return result.user.id;
            })
            .catch(function (error) {
                console.log(error);
            });
    }
});

Vue.component('app-footer', {
    template: `
    <footer>
        <div class="container">
            <p>Copyright &copy; Flask Inc.</p>
        </div>
    </footer>
    `
});

const Logout = Vue.component('logout', {
    template: `
    <div>Logging out...</div>
    `,
    methods: {
        logOut: function () {
            let self = this;
            fetch("/api/auth/logout", { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') }})
                .then(function (response) {
                    return response.json();
                })
                .then(function (response) {
                    let result = response.data;
                    alert(result.user.username + " logged out!")
                    sessionStorage.removeItem('token');
                    console.info('Token removed from sessionStorage.');
                    router.push("/")
                    location.reload()
                })
                .catch(function (error) {
                    console.log(error);
                })
        }
    },

    beforeMount(){
        this.logOut()
    }
});

const Home = Vue.component('home', {
   template: `
    <div id="home_page">
        <div id="main">
            <h2> Buy and Sell Cars Online </h2>
            </br>
            <p>United Auto Sales provides the fastest, easiest and most user friendly way to buy or sell cars online. Find a Great Price on the Vehicle You Want.</p>
            <hr>
            <button id="home_btn1" @click="$router.push('register')" type="button" class="btn btn-success">Register</button>
            <button id="home_btn2" @click="$router.push('login')" type="button" class="btn btn-primary">Login</button>
        </div>
        <div id="home_img">
            <img src="/static/images/photo-1568605117036-5fe5e7bab0b7.jpg">
        </div>
    </div>
   `,
    data: function() {
       return {}
    }
});

const Register = Vue.component('register', {
    template: `
     <div id="registration">
        <h2 id="reg_head">Register</h2>
        <div>{{messages}}</div>
        <div id="reg">
            <form @submit.prevent="regForm" method="POST" enctype="multipart/form-data" id="reg_form">
                <p class="reg_form">
                    <label for="username">Username:</label> <br>
                    <input class="form_ele" name="username" required placeholder="Enter username">
                </p>

                <p class="reg_form">
                    <label for="password">Password:</label> <br>
                    <input name="password" type="password" class="form_ele" required placeholder="Enter password">
                </p>

                <p class="reg_form">
                    <label for="name">Name:</label> <br>
                    <input name="name" class="form_ele" required placeholder="Name">
                </p>

                <p class="reg_form">
                    <label for="email">Email:</label> <br>
                    <input name="email" class="form_ele" required placeholder="Enter email">
                </p>

                <p class="reg_form">
                    <label for="location">Location:</label> <br>
                    <input name="location" class="form_ele" required placeholder="Enter location">
                </p>

                <p class="reg_form">
                    <label for="biography">Biography:</label> <br>
                    <textarea name="biography" class="form_ele" placeholder="add multiple lines"></textarea>
                </p>

                <p class="reg_form">
                    <label for="photo">Photo:</label> <br>
                    <input id="photo" type="file" name="photo">
                </p>

                <button type="submit" id="reg_button" class="btn btn-success">Register</button>

            </form>
        </div>
     </div>
    `,
     data: function() {
        return {
            messages: ''
        }
     },

     methods: {
        regForm: function(){
            //console.log("hi hello")
            let self = this;
            let reg_form = document.getElementById('reg_form');
            let form_data = new FormData(reg_form);
            fetch("/api/register", { method: 'POST', body: form_data, headers: { 'X-CSRFToken': token }, credentials: 'same-origin'}).then(function (response) {
                return response.json();
                }).then(function (jsonResponse) {
                    // display a success message
                    console.log(jsonResponse);
                    self.messages = jsonResponse;
                    alert("User Registered!")
                    router.push("login")
                }).catch(function (error) {
                        console.log(error);
                    });
        }
     }
 });

 const Login = Vue.component('login', {
    template: `
     <div id="login">
        <h2 id="log_head">Login</h2>
        <div>{{messages}}</div>
        <div id="log">
            <form @submit.prevent="loginForm" method="POST" id="log_form">

                <p class="log_info">
                    <label  id="log_u" for="username">Username:</label> <br>
                    <input name="username" class="log_ele" required placeholder="Enter username">
                </p>

                <p class="log_info">
                    <label for="password">Password:</label> <br>
                    <input name="password" type="password" class="log_ele" required placeholder="Enter password">
                </p>

                <button id="log_button" type="submit" class="btn btn-success">Login</button>

            </form>
        </div>
     </div>
    `,
     data: function() {
        return {
            messages: '',
            token: ''
        }
     },

    methods: {
        loginForm: function(){
            let self = this;
            let log_form = document.getElementById('log_form');
            let form_data = new FormData(log_form);
            fetch("/api/auth/login", { method: 'POST', body: form_data, headers: { 'X-CSRFToken': token }, credentials: 'same-origin'}).then(function (response) {
                return response.json();
                }).then(function (jsonResponse) {
                    // display a success message
                    console.log(jsonResponse);
                    self.messages = jsonResponse;
                    let jwt_token = jsonResponse.data.token;

                    // We store this token in sessionStorage so that subsequent API requests
                    // can use the token until it expires or is deleted.
                    sessionStorage.setItem('token', jwt_token);
                    console.info('Token generated and added to sessionStorage.');
                    self.token = jwt_token;
                    alert("Logged In!")
                    router.push("explore")
                    location.reload()
                }).catch(function (error) {
                        console.log(error);
                    });
        }
     }
 });

 const Explore = Vue.component('explore', {
    template: `
    <div id="explore">
        <h2> Explore </h2>
        <div id="search">
            <form @submit.prevent="exp_search" method="GET" id="exp_search">
                <div class="left">
                    <label for="make">Make</label>
                    <input name="make" type="text" class="exp_ele">
                </div>
                <div class="right">
                    <label for="model">Model</label>
                    <input name="model" type="text" class="exp_ele">
                    <button id="exp_button" type="submit" class="btn btn-success">Search</button>
                </div>
            </form>
        </div>
        <div id="exp">
            <ul>
                <li v-for="car in allcars">
                    <div id="explore_blank">
                        <img id="car_photo" :src="'/static/uploads/' + car.photo" alt="user post">
                        <h4> {{car.year}} {{car.make}} </h4>
                        <p> {{car.model}} </p>
                        <button @click="$router.push('/cars/{{car.id}}')" class="btn btn-success"> View More Details </button>
                    </div>
                </li>
            </ul>

        </div>
    </div>
   `,
     data: function() {
        return {
            allcars: [],
            userid: 0
        }
     },

     methods: {
        exp_search: function(postid){
            console.log(postid);
            let likephoto = document.getElementById('likephoto');
            let form_data = new FormData(likephoto);
            fetch("/api/cars/" + postid + "/like", { method: 'POST', body: form_data, headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }, credentials: 'same-origin'})
            .then(function (response) {
                return response.json();
                }).then(function (jsonResponse) {
                    // display a success message
                    alert("Photo liked!");
                    this.pagestart;
                    location.reload();
                    console.log(jsonResponse.message);
                }).catch(function (error) {
                        console.log(error);
                    });
        },

        profile: function(userid){ 
            this.$router.push("/users/"+userid)
           
        },

        pagestart: function(){
            let self = this;
            fetch('/api/secure', {
                'headers': {
                    'Authorization': 'Bearer ' + sessionStorage.getItem('token')
                }
            }).then(function (response) {
                    return response.json();
                }).then(function (response) {
                    let result = response.data;
                    console.log("User ID retrieved");
                    self.userid = result.user.id;
                    return result.user.id;
                }).then( function(user_id){
                    //let self = this;
                    fetch("/api/cars", { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') }})
                    .then(function (response) {
                        return response.json();
                        })
                        .then(function (jsonResponse) {
                            // display a success message
                            self.allcars = jsonResponse;
                            console.log(jsonResponse);
                        })
                        .catch(function (error) {
                                console.log(error);
                            });
                }).catch(function (error) {
                    console.log(error);
                })
         }
     },

     created: function(){
         this.pagestart();
     }
 });

 const MyProfile = Vue.component('myprofile', {
    props: ['user_id'],
    template: `
     <div id="myprofile">
        <div id="mypro">

            <div id="mypro_info">

                <div id="mypro_image">
                    <img id="mypro_img" :src="'/static/uploads/' + photo" alt="profile img">  
                </div>

                <div id="mypro_perdata">
                    <h3>
                        {{name}}
                    </h3>

                    <p id="username">
                        @{{username}}
                    </P>

                    <p>
                        {{biography}}
                    </p>
                    
                    <p>
                        Email: {{email}}
                    </p>

                    <p id="location_info">
                        Location: {{location}}
                    </p>

                    <p id="member_info">
                        Joined: {{date_joined}}
                    </p>
                </div>

            </div>

            <div id="mypro_images">
                <h2> Cars Favourited </h2>
                <ul>
                    <li v-for="post in cars">
                        <img id="img_box" v-bind:src="'/static/uploads/' + post"/>
                    </li>
                </ul>
            </div>
            <!--<img src="/static/js/test.jpg"/>-->
        </div>
     </div>
    `,
     data: function() {
        return {
            cars: [],
            photo: '',
            name: '',
            email: '',
            username: '',
            biography: '',
            date_joined: '',
            location: '',
            current_user_id: 0
        }
     },

     created: function(){
        this.retrieveUser();
     },

     methods: {
        retrieveUser: function(){
            let self = this;
            fetch('/api/secure', {
                'headers': {
                    'Authorization': 'Bearer ' + sessionStorage.getItem('token')
                }
            }).then(function (response) {
                    return response.json();
                }).then(function (response) {
                    let result = response.data;
                    console.log("User ID retrieved");
                    console.log(self.user_id);
                    self.current_user_id = result.user.id;
                    console.log(self.current_user_id);
                    return self.user_id; //gettting from prop
                    //self.user_id = result.user.id
                    //return result.user.id
                }).then( function(user_id){
                    //let self = this;
                    fetch("/api/users/" + user_id, { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') }})
                    .then(function (response) {
                        return response.json();
                        })
                        .then(function (jsonResponse) {
                            // display a success message
                            console.log(jsonResponse);
                            self.cars = jsonResponse.cars;
                            self.name = jsonResponse.name;
                            self.photo = jsonResponse.photo;
                            self.location = jsonResponse.location;
                            self.date_joined = jsonResponse.date_joined;
                            self.biography = jsonResponse.biography;
                            self.email = jsonResponse.email;
                            self.username = jsonResponse.username;
                        })
                        .catch(function (error) {
                                console.log(error);
                            });
                }).catch(function (error) {
                    console.log(error);
                })
        },
     }
 });

//  const Car = Vue.component('car', {
//     props: ['user_id'],
//     template: `
//      <div id="car">
//         <div id="mypro">

//             <div id="mypro_info">

//                 <div id="mypro_image">
//                     <img id="mypro_img" :src="'/static/uploads/' + photo" alt="profile img">  
//                 </div>

//                 <div id="mypro_perdata">
//                     <h3>
//                         {{name}}
//                     </h3>

//                     <p id="username">
//                         @{{username}}
//                     </P>

//                     <p>
//                         {{biography}}
//                     </p>
                    
//                     <p>
//                         Email: {{email}}
//                     </p>

//                     <p id="location_info">
//                         Location: {{location}}
//                     </p>

//                     <p id="member_info">
//                         Joined: {{date_joined}}
//                     </p>
//                 </div>

//             </div>

//             <div id="mypro_images">
//                 <h2> Cars Favourited </h2>
//                 <ul>
//                     <li v-for="post in cars">
//                         <img id="img_box" v-bind:src="'/static/uploads/' + post"/>
//                     </li>
//                 </ul>
//             </div>
//             <!--<img src="/static/js/test.jpg"/>-->
//         </div>
//      </div>
//     `,
//      data: function() {
//         return {
//             description: '',
//             make: '',
//             model: '',
//             colour: '',
//             year: '',
//             transmission: '',
//             car_type: '',
//             price: '',
//             photo: '',
//             current_user_id: 0
//         }
//      },

//      created: function(){
//         this.retrieveCar();
//      },

//      methods: {
//         retrieveCar: function(){
//             let self = this;
//             fetch('/api/secure', {
//                 'headers': {
//                     'Authorization': 'Bearer ' + sessionStorage.getItem('token')
//                 }
//             }).then(function (response) {
//                     return response.json();
//                 }).then(function (response) {
//                     let result = response.data;
//                     console.log("User ID retrieved");
//                     console.log(self.user_id);
//                     self.current_user_id = result.user.id;
//                     console.log(self.current_user_id);
//                     return self.user_id; //gettting from prop
//                     //self.user_id = result.user.id
//                     //return result.user.id
//                 }).then( function(user_id){
//                     //let self = this;
//                     fetch("/api/cars/" + user_id, { method: 'GET', headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token') }})
//                     .then(function (response) {
//                         return response.json();
//                         })
//                         .then(function (jsonResponse) {
//                             // display a success message
//                             console.log(jsonResponse);
//                             self.description = jsonResponse.description;
//                             self.make = jsonResponse.make;
//                             self.model = jsonResponse.model;
//                             self.colour = jsonResponse.colour;
//                             self.year = jsonResponse.year;
//                             self.car_type = jsonResponse.car_type;
//                             self.transmission = jsonResponse.transmission;
//                             self.price = jsonResponse.price;
//                             self.photo = jsonResponse.photo;
//                         })
//                         .catch(function (error) {
//                                 console.log(error);
//                             });
//                 }).catch(function (error) {
//                     console.log(error);
//                 })
//         }
//      }
//  });

 const NewCar = Vue.component('newcar', {
    template: `
     <div id="newcar">
        <h2 id="newp_head">Add New Car</h2>
        <div class="car_form">
            <form @submit.prevent="newCar" method="POST" enctype="multipart/form-data" id="new_car">
            
                <p class="newcar_info">
                    <label for="make">Make:</label> <br>
                    <input name="make" type="text">
                </p>

                <p class="newcar_info">
                    <label for="model">Model:</label> <br>
                    <input name="model" type="text">
                </p>

                <p class="newcar_info">
                    <label for="colour">Colour:</label> <br>
                    <input name="colour" type="text">
                </p>
                        
                <p class="newcar_info">
                    <label for="year">Year:</label> <br>
                    <input name="year" type="text">
                </p>
                
                <p class="newcar_info">
                    <label for="price">Price:</label> <br>
                    <input name="price" type="text">
                </p>

                <p class="newcar_info">
                    <label for="car_type">Car Type:</label> <br>
                    <input name="car_type" type="text">
                </p>

                <p class="newcar_info">
                    <label for="transmission">Transmission:</label> <br>
                    <input name="transmission" type="text">
                </p>

                <p class="newcar_info">
                <label for="description">Description:</label> <br>
                <textarea name="description"></textarea>
                </p>
                
                <p class="newcar_info">
                <label id="newp_photo" for="photo">Photo:</label> <br>
                <input id="newp_ele" type="file" name="photo">
                </p>
                                
                <button id="newp_button" type="submit" class="btn btn-success">Submit</button>
            </form>
        </div>
     </div>
    `,
     data: function() {
        return {
            messages: '',
            result: ''
        }
     },

     methods: {
        newCar: function () {
            let self = this;
            fetch('/api/secure', {
                'headers': {
                    'Authorization': 'Bearer ' + sessionStorage.getItem('token')
                }
            }).then(function (response) {
                    return response.json();
                }).then(function (response) {
                    let result = response.data;
                    console.log("User ID retrieved");
                    self.user_id = result.user.id
                    return result.user.id
                }).then( function(user_id){
                    let self = this;
                    let new_car = document.getElementById('new_car');
                    let form_data = new FormData(new_car);
                    fetch("/api/cars", { method: 'POST', body: form_data, headers: { 'Authorization': 'Bearer ' + sessionStorage.getItem('token'), 'X-CSRFToken': token }, credentials: 'same-origin'}).then(function (response) {
                        return response.json();
                        }).then(function (jsonResponse) {
                            // display a success message
                            console.log(jsonResponse);
                            alert("Car successfully uploaded!");
                            router.push("/explore")
                            self.messages = jsonResponse;
                        }).catch(function (error) {
                                console.log(error);
                            });
                }).catch(function (error) {
                    console.log(error);
                })
        }
     }
 });

const NotFound = Vue.component('not-found', {
    template: `
    <div>
        <h1>404 - Not Found</h1>
    </div>
    `,
    data: function () {
        return {}
    }
})

// Define Routes
const router = new VueRouter({
    mode: 'history',
    routes: [
        {path: "/", component: Home},
        // Put other routes here
        {path: "/register", component: Register},

        {path: "/login", component: Login},

        {path: "/logout", component: Logout},

        {path: "/explore", component: Explore},

        {path: "/users/:user_id", component: MyProfile, props: true},
        
        {path: "/cars/new", component: NewCar},
        
        {path: "/cars/:car_id", component: Car, props: true},

        // This is a catch all route in case none of the above matches
        {path: "*", component: NotFound}
    ]
});

// Instantiate our main Vue Instance
let app = new Vue({
    el: "#app",
    router
});
