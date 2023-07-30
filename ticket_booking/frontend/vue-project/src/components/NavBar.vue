<template>
  <v-app-bar app color="black" dark class="custom-navbar">
    <!-- Navbar logo or title (you can customize this) -->
    <v-toolbar-title class="navbar-title">My App</v-toolbar-title>

    <!-- Spacer to push items to the right -->
    <v-spacer></v-spacer>

    <!-- Search bar -->
    <form class="form-inline my-2 my-lg-0" @submit.prevent="submitSearch">
      <div class="input-group">
        <input type="text" class="form-control" placeholder="Search movies" v-model="searchQuery">
        <div class="input-group-append">
          <button class="btn btn-pink mt-0" type="submit">Search</button>
        </div>
      </div>
    </form>

    <!-- Check if the user is logged in, show appropriate options -->
    <template v-if="isLoggedIn">
      <!-- Display username or 'Guest' -->
      <v-chip color="pink" text-color="black"><router-link class="nav-link" to="/userdashboard">Your Account</router-link></v-chip>
      <!-- <v-btn v-if="isLoggedIn" @click="logout" color="pink" text-color="black">Logout</v-btn> -->
      <button class="nav-item nav-link clickable-element" @click="logout" v-if="isLoggedIn">Logout</button>
    </template>
    <template v-else>
      <v-btn v-if="!isLoggedIn && $route.path != '/login'" @click="login" color="pink" text-color="black">Login</v-btn>

      <v-btn @click="register" color="pink" text-color="black">Register</v-btn>


    </template>
  </v-app-bar>
</template>

<script>



export default {
  data() {
    return {
      searchQuery: '',
  
    };
  },
  computed: {
    isLoggedIn() {
      // Check if an access token is present in session storage
      const accessToken = sessionStorage.getItem('access_token') || localStorage.getItem('access_token');
      console.log(accessToken)
      return !!accessToken; // Return true if the access token is present, false otherwise
    }
  },
  methods: {
    login() {

      this.$router.push('/login');
      // this.isLoggedIn = true;

    },
    register() {

      this.$router.push('/register');
      // this.isLoggedIn = true;

    },
    async logout() {
      try {
        // Check if an access token is available in sessionStorage or localStorage
        const access_token = sessionStorage.getItem('access_token') || localStorage.getItem('access_token');

        if (!access_token) {
          console.error('Logout failed: Access token not found.');
          return;
        }
        const headers = {
          Authorization: `Bearer ${access_token}`,
        };

        // Send a POST request to the 'logout' endpoint using Axios (or any HTTP client of your choice)
        const response = await this.$http.post('logout', null, { headers });
        if (response.status === 200) {
          // Clear both sessionStorage and localStorage
          sessionStorage.clear();
          localStorage.clear();
          this.$router.push('/');
          window.location.reload();
        } else {
          console.log('Logout failed: Unexpected response status.');
        }
      } catch (error) {
        console.error('Logout error:', error);
      }
    },
    submitSearch() {
      // Handle search query submission logic here
      // For example, perform a search based on the searchQuery
      // For simplicity, we'll just log the searchQuery to the console
      console.log('Search query:', this.searchQuery);
    },
  },
};
</script>

<style>
/* Add any custom styles for the navbar here */
.custom-navbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  /* background-color: #ff4081; */
}

.navbar-title {
  font-size: 24px;
  font-weight: bold;
}

.form-control {
  /* background-color: #000;  */
  color: #fff;
}

.btn-pink {
  background-color: #ff4081;
  /* Pink */
  color: #000;
}

.btn-pink:hover {
  background-color: #ff80ab;
  /* Lighter Pink */
}

.v-chip {
  background-color: #ff4081;
  /* Pink */
  color: #000;
  font-size: 14px;
  font-weight: bold;
}

.v-btn {
  font-size: 14px;
  font-weight: bold;
}

.v-btn:hover {
  background-color: #ff80ab;
  /* Lighter Pink */
}</style>
