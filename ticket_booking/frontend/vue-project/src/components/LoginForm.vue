<template>
  <form @submit.prevent="submitLoginForm">
    <div class="form-group">
      <label for="email">Email address</label>
      <input v-model="email" type="email" class="form-control" id="email" aria-describedby="emailHelp"
        placeholder="Enter email" required>
    </div>
    <div class="form-group">
      <label for="password">Password</label>
      <input v-model="password" type="password" class="form-control" id="password" placeholder="Password" required>
    </div>
    <button type="submit" class="btn btn-primary">Login</button>
  </form>
</template>
  
<script>
export default {
  data() {
    return {
      email: '',
      password: '',
    };
  },
  computed: {
    loginData() {
      return {
        email: this.email,
        password: this.password,
      };
    },
  },
  methods: {
    async submitLoginForm() {
      try {
        const response = await this.$http.post('login', this.loginData);

        if (response.status === 200) {
          // const name = this.name;
          const email = this.email;
          const access_token = response.data.access_token;
          console.log(access_token);


          const storage = this.rememberMe ? localStorage : sessionStorage;
          storage.setItem('name', name);
          storage.setItem('email', email);
          storage.setItem('access_token', access_token);

          this.$router.push('/'); // Redirect to the homepage after login
          window.location.reload()
        } else if (response.status === 401) {
          window.alert("Your email or password is incorrect");
          console.log(data);
          this.loginStatus = 'error';
        } else {
          // Handle other response status codes if needed
          this.loginStatus = 'error';
        }
      } catch (error) {
        console.error('An error occurred:', error);
        this.loginStatus = 'error';
      }
    },
  },
};
</script>
  
<style>
/* Add any custom styles for the login form here */
.secondary {
  background-color: #E91E63;
  /* Pink color */
  color: #fff;
  /* White text color */
}

.primary {
  background-color: #1976D2;
  /* Blue color */
  color: #fff;
  /* White text color */
}</style>
  